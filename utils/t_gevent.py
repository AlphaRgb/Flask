#!/usr/bin/env python3
# coding=utf-8

# flask结合gevent支持多并发

from flask import Flask
from gevent import monkey
from gevent.pywsgi import WSGIServer

monkey.patch_all()

app = Flask(__name__)


@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    # app.run(threaded=True)
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
