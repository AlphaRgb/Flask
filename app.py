#!/usr/bin/env python3
# coding: utf-8

from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return 'hello world'


@app.route('/<int:post_id>/')
def post(post_id):
    return 'post_id %s' % post_id


if __name__ == '__main__':
    app.run(debug=True)
