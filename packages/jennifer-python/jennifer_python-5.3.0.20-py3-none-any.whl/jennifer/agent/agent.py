import threading
import logging
import json
import os
import sys
import zlib
import traceback
from jennifer.recorder import Recorder
from jennifer.api import task
import socket
import struct
import time
from random import random
from .transaction import Transaction

record_types = {
    'method': 1,
    'sql': 2,
    'event_detail_msg': 3,
    'service': 4,
    'txcall': 5,
    'browser_info': 6,
    'thread_name': 7,
    'thread_stack': 8,
    'user_id': 9,
    'dbc': 10,
    'stack_trace': 11,
    'count': 12,
}


class Agent(object):
    def __init__(self):
        self.transactions = []
        self.inst_id = -1
        self.recorder = None
        self.master_lock = threading.Lock()
        self.logger = logging.getLogger('jennifer')
        self.config_pid = 0
        self.address = ''
        self.masterConnection = None

        # uwsgi 호스팅인 경우 --enable-threads 옵션이 지정되지 않은 상황이라면,
        # run_timer 등의 스레드 관련 기능이 동작하지 않으므로 사후 처리를 해야 함. (TODO: 아직 미구현)
        self.thread_enabled = False

    @staticmethod
    def gen_new_txid():
        return int(str(int(random() * 100)) + str(Agent.current_time()))

    @staticmethod
    def current_thread_id():
        return threading.get_ident()

    @staticmethod
    def current_cpu_time():
        if hasattr(time, 'process_time'):
            return int(time.process_time() * 1000)
        return int(time.clock() * 1000)

    def current_transaction(self):
        ret = None
        thread_id = self.current_thread_id()
        for t in self.transactions:
            if t.thread_id == thread_id:
                ret = t
                break
        return ret

    # config.address == /tmp/jennifer-...sock
    # config.log_path == /tmp/jennifer-python-agent.log
    def set_config(self, config):
        self.address = config['address']
        self.recorder = Recorder()
        self.config_pid = os.getpid()

        # print("os.environ:", os.environ['JENNIFER_MASTER_ADDRESS'])

        ret = None
        with self.master_lock:
            ret = self.connect_master()

        if ret:
            task.run_timer(self.process_agent_metric)

    @staticmethod
    def debug_log(text):
        if os.getenv('PY_DBG'):
            try:
                log_socket = __import__('jennifer').get_log_socket()
                if log_socket is not None:
                    log_socket.log(text)
            except ModuleNotFoundError as e:
                print(e)

    def connect_master(self) -> bool:
        self.masterConnection = None
        if not os.path.exists(self.address):
            return False

        try:
            self.masterConnection = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.masterConnection.connect(self.address)

            self.handshake_to_master()
            task.run_task(self.master_loop)
            return True
        except ConnectionRefusedError as e:
            self.masterConnection = None
            Agent.debug_log('connect_master error')
            return False

    def handshake_to_master(self):
        version = b'{"version":1,"pid":' + str(os.getpid()).encode('utf-8') + b'}'
        self.masterConnection.send(b'\x08jennifer' + struct.pack('>L', len(version)) + version)

    def master_loop(self):

        while True:
            if self.masterConnection is None:
                break

            try:
                byte_cmd_len = self.masterConnection.recv(1)
                if len(byte_cmd_len) < 1:
                    break  # failed to connect master

                cmd_len = ord(byte_cmd_len)
                cmd = self.masterConnection.recv(cmd_len)
                param_len, = struct.unpack('>L', self.masterConnection.recv(4))
                try:
                    param = json.loads(self.masterConnection.recv(param_len))
                except:
                    continue

                if cmd == b'active_detail':
                    txid = param.get('txid')
                    request_id = param.get('request_id')
                    if txid is not None and request_id is not None:
                        data = self.get_active_service_detail(txid)
                        if data is not None:
                            data['request_id'] = request_id
                            self.send_to_master('active_detail', data)
                            # Agent.debug_log('active_detail callback' + str(data))

            except (BrokenPipeError, OSError):
                break

    def get_active_service_detail(self, txid):
        ret = None
        cpu_time = self.current_cpu_time()
        current_time = self.current_time()

        for t in self.transactions:
            if t.txid == txid:
                stack = 'Fail to get a callstack'
                frame = sys._current_frames().get(t.thread_id)
                if frame is not None:
                    stack = ''.join(traceback.format_stack(frame))
                ret = {
                    'txid': t.txid,
                    'thread_id': t.thread_id,
                    'service_name': t.path_info,
                    'elapsed': current_time - t.start_time,
                    'method': t.request_method,
                    'http_query': t.query_string,
                    'sql_count': t.sql_count,
                    'sql_time': t.sql_time,
                    'tx_time': t.external_call_time,
                    'tx_count': t.external_call_count,
                    'fetch_count': t.fetch_count,
                    'cpu_time': cpu_time - t.start_system_time,
                    'start_time': t.start_time,
                    'stack': stack,
                }

        return ret

    def process_agent_metric(self):
        # Agent.debug_log('process_agent_metric called!')
        metrics = self.recorder.record_self()
        self.send_to_master('record_metric', metrics)

        current = Agent.current_time()
        current_cpu = Agent.current_cpu_time()

        self.send_to_master('active_service_list', {
            'active_services': [
                t.to_active_service_dict(current, current_cpu)
                for t in self.transactions
            ],
        })

    def send_to_master(self, cmd, params):
        if os.getpid() != self.config_pid:
            self.set_config({
                'address': self.address
            })

        try:
            p = json.dumps(params, default=str).encode('utf-8')
            pack = struct.pack('>B', len(cmd)) + cmd.encode('utf-8') + struct.pack('>L', len(p)) + p
            with self.master_lock:
                if self.masterConnection is None:
                    if not self.connect_master():
                        return
                self.masterConnection.send(pack)
                # print("send_to_master", cmd)
        except (BrokenPipeError, OSError):
            self.masterConnection = None

    @staticmethod
    def current_time():
        return int(time.time() * 1000)

    @staticmethod
    def current_cpu_time():
        if hasattr(time, 'process_time'):
            return int(time.process_time() * 1000)
        return int(time.clock() * 1000)

    def start_transaction(self, environ, wmonid, wsgi_handler_name=None, start_time=None):
        if start_time is None:
            start_time = Agent.current_time()
        txid = Agent.gen_new_txid()
        transaction = Transaction(
            agent=self,
            start_time=start_time,
            txid=txid,
            environ=environ,
            wmonid=wmonid,
        )
        self.transactions.append(transaction)
        transaction.start_system_time = Agent.current_cpu_time()

        self.send_to_master('start_transaction', {})
        return transaction

    def end_transaction(self, transaction: Transaction):
        try:
            self.transactions.remove(transaction)

            self.send_to_master('end_transaction', {
                'transaction': transaction.to_dict(),
                'profiler': transaction.profiler.to_dict(),
            })

            # uwsgi 환경의 --enable-threads 옵션이,
            #  없는 경우를 위한 처리 추가
            #  있는 경우에는 어차피 run_timer 내에서 처리
            # if self.number_of_requests == 0:
            #    self.process_agent_metric()
        except ValueError:
            pass

    @staticmethod
    def _hash_text(text):
        hash_key = zlib.crc32(text.encode('utf-8'))
        if hash_key > 0x7FFFFFFF:
            return (hash_key & 0x7FFFFFFF) * -1
        return hash_key

    def hash_text(self, text, hash_type='service'):
        if text is None or len(text) == 0:
            return 0

        self.send_to_master('record_text', {
            'type': record_types.get(hash_type, 0),
            'text': text,
        })

        return self._hash_text(text)
