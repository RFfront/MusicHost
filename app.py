from pprint import pprint,pformat
import socket
import threading
from flask import Flask, Response, copy_current_request_context, render_template, session, request
import subprocess
from models import *

from vkmusget import LoongPoool
port = 5001

app = Flask(__name__)



def openBrowser(http):
    subprocess.call(f"start {http}",
                    creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)


@app.route('/newMsgVK', methods=["POST"])
def msg_vk_wrap():
    VKMessages(**request.get_json()).save()
    return Response(status=200)

@app.get('/threads')
def getThreads():
    return pformat(list(threading.enumerate()))

def retIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


@app.route('/hello')
def hello():
    return render_template('index.html', context=(retIP(), port))

if __name__ == '__main__':
    thread = threading.Thread(target=LoongPoool, daemon=True)
    thread.start()
    # openBrowser(f"http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
