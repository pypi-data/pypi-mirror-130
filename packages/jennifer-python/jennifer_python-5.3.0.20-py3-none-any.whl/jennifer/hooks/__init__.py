import os
import sys

from jennifer.agent import jennifer_agent
# from . import app_flask, , , external_urllib
from . import app_flask
from . import db_sqlite3
from . import app_django
from . import db_mysqlclient
from . import db_pymysql
from . import external_requests
from . import external_urllib

HOOK_SUPPORT_LIST = [
    app_flask,
    app_django,
    db_mysqlclient,
    db_pymysql,
    db_sqlite3,
    external_urllib,
    external_requests,
]


def is_module_exist(module):
    try:
        return __import__(module)
    except ImportError:
        return False


def hooking():
    for m in HOOK_SUPPORT_LIST:
        module = is_module_exist(m.__hooking_module__)
        if module is not False:
            m.hook(module)
        # else:
        #     module_names = set(sys.modules) & set(globals())
        #     all_modules = [sys.modules[name] for name in module_names]
        #     debug_log(str(all_modules))

    hook_builtins()


# Socket Open/Connect 가로채기
def hook_builtins():
    import socket
    __builtins__['open'] = wrap_file_open(__builtins__['open'])
    socket.socket.connect = wrap_socket_connect(socket.socket.connect)
    socket.socket.connect_ex = wrap_socket_connect(socket.socket.connect_ex)


def wrap_file_open(origin_open):
    agent = jennifer_agent()

    def handler(file_path, mode='r', *args, **kwargs):
        transaction = agent.current_transaction()

        if transaction is not None and 'site-packages' not in file_path:
            transaction.profiler.file_opened(
                name=os.path.abspath(os.path.join(os.getcwd(), file_path)),
                mode=mode
            )
        return origin_open(file_path, mode, *args, **kwargs)

    return handler


def wrap_socket_connect(origin_connect):
    import socket
    agent = jennifer_agent()

    def handler(self, address):
        transaction = agent.current_transaction()

        ret = origin_connect(self, address)

        if self.family != socket.AF_INET:
            return ret

        if transaction is not None:
            remote_address = self.getpeername()
            local_address = self.getsockname()
            transaction.profiler.socket_opened(
                host=remote_address[0],
                port=remote_address[1],
                local=local_address[1],
            )
        return ret

    return handler


def debug_log(text):
    if os.getenv('PY_DBG'):
        try:
            log_socket = __import__('jennifer').get_log_socket()
            if log_socket is not None:
                log_socket.log(text)
        except ModuleNotFoundError as e:
            print(e)