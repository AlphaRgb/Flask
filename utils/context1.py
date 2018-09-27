#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: AlphaFF
# @Date:   2018-08-03 10:01:36
# @Email: liushahedi@gmail.com
# @Last Modified by:   AlphaFF
# @Last Modified time: 2018-08-03 21:37:08


import logging
from flask import Flask, g, request, current_app, template_rendered, render_template
import pymysql
from flask_mail import Mail, Message
from celery import Celery


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY='hard to guess string',
    DEBUG=True,
    MAIL_SERVER='smtp.163.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='liushahedi@163.com',
    MAIL_PASSWORD='31415926fw',
    MAIL_DEFAULT_SENDER='JamesBy <liushahedi@163.com>',
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/1',
    CELERY_TASK_SERIALIZER='pickle',
    CELERY_ACCEPT_CONTENT=['pickle']
))

mail = Mail(app)


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


# celery部分
# celery = make_celery(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def send_async_email(msg):
    with app.app_context():
        logger.info('send email...')
        mail.send(msg)


@celery.task
def test_celery():
    logger.warning('test celery once..')


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
    msg = Message('Hello Celery!', recipients=['804950408@qq.com'])
    msg.body = 'test celery...'
    # mail.send(msg)
    send_async_email.delay(msg)
    # test_celery.delay()
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
a

