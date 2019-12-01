#!/usr/bin/env python3
# coding: utf-8

from flask import Flask, request
app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    app.logger.info('request.headers:{}'.format(request.headers))
    app.logger.info('hahahah')
    app.logger.warning('request data:{}'.format(request.get_json()))
    return 'hello world'


@app.route('/<int:post_id>/')
def post(post_id):
    return 'post_id %s' % post_id


if __name__ == '__main__':
    app.run()
