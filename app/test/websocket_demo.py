# -*- coding: utf-8 -*-

import websocket

try:
    import thread
except ImportError:
    import _thread as thread
import time


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### Closed ###")


def on_open(ws):
    def run(*args):
        for i in range(10):
            time.sleep(1)
            data = input("输入弹幕:")
            ws.send("Hello websocket {0}, {1}".format(i, data))
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == '__main__':
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://123.207.167.163:9010/ajaxchattest",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
