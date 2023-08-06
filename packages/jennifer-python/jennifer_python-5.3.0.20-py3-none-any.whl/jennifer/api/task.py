import os
from threading import Thread, Timer
import time


def run_task(target, args=()):
    t = Thread(target=target, args=args)
    t.daemon = True
    t.start()
    return t


def run_timer(target_func, interval=1):

    def handler():
        while True:
            try:
                target_func()
                time.sleep(interval)
            except:
                pass

    t = Thread(target=handler)
    t.daemon = True
    t.start()

    return t


def debug_log(text):
    # print(text)
    if os.getenv('PY_DBG'):
        try:
            log_socket = __import__('jennifer').get_log_socket()
            if log_socket is not None:
                log_socket.log(text)
        except ModuleNotFoundError as e:
            print(e)
