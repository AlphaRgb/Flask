#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: AlphaFF
# @Date:   2018-08-03 10:01:36
# @Email: liushahedi@gmail.com
# @Last Modified by:   AlphaFF
# @Last Modified time: 2018-08-03 11:41:06


import logging
from flask import Flask, g, request, current_app, template_rendered, render_template
import pymysql

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def get_db():
    if not hasattr(g, 'conn'):
        g.conn = pymysql.connect(host='127.0.0.1', user='root', db='test')
    return g.conn


@app.before_first_request
def connect_db():
    logger.info('before first request')
    # g.conn = pymysql.connect(host='127.0.0.1', user='root', db='test')


@app.before_request
def before_request():
    logger.info('before request started')
    g.conn = get_db()
    logger.info(request.url)
    logger.info(g.conn)


@app.before_request
def before_request2():
    logger.info('before request started 2')
    logger.info(request.url)
    g.name = 'SampleApp'


@app.after_request
def after_request(response):
    logger.info('after request finished')
    logger.info(request.url)
    response.headers['key'] = 'value'
    logger.info(response)
    return response


@app.teardown_request
def teardown_request(exception):
    logger.info('teardown request')
    logger.info(request.url)
    # logger.info('close SQL conn')
    # g.conn.close()


@app.route('/')
def index():
    logger.info('current app name %s', current_app.name)
    return 'Hello, %s' % g.name


@app.route('/hello/')
def hello():
    return render_template('hello.html')


# 信号装饰器
@template_rendered.connect_via(app)
def with_template_rendered(sender, template, context, **extra):
    logger.info('Using template: %s with context: %s' % (template.name, context))
    logger.info(request.url)


@app.teardown_appcontext
def teardown_db(exception):
    logger.info('teardown application...')
    logger.info('close SQL conn')
    if hasattr(g, 'conn'):
        g.conn.close()


if __name__ == '__main__':
    app.run(debug=True)
