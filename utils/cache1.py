#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: AlphaFF
# @Date:   2018-08-04 09:36:42
# @Email: liushahedi@gmail.com
# @Last Modified by:   AlphaFF
# @Last Modified time: 2018-08-04 10:50:39

from functools import wraps
from werkzeug.contrib.cache import SimpleCache
from flask import Flask, request
from flask_cache import Cache


app = Flask(__name__)

# # 自定义的缓存装饰器
# cache = SimpleCache()


# def cached(timeout=1 * 60, key='view_%s'):
#     def decorator(f):
#         @wraps(f)
#         def wrapper(*args, **kw):
#             cache_key = key % request.path
#             value = cache.get(cache_key)
#             if value is None:
#                 value = f(*args, **kw)
#                 cache.set(cache_key, value, timeout=timeout)
#             return value
#         return wrapper
#     return decorator


# @app.route('/')
# @cached()
# def hello():
#     print('view hello called')
#     return 'hello worlds'

cache = Cache(app, config={
    'CACHE_TYPE': 'simple'
})

# 第三方缓存服务器
# cache = Cache(app, config={'CACHE_TYPE': 'redis',          # Use Redis
#                            'CACHE_REDIS_HOST': 'abc.com',  # Host, default 'localhost'
#                            'CACHE_REDIS_PORT': 6379,       # Port, default 6379
#                            'CACHE_REDIS_PASSWORD': '111',  # Password
#                            'CACHE_REDIS_DB': 2}            # DB, default 0


@app.route('/')
@cache.cached(timeout=300, key_prefix='view_%s', unless=None)
def index():
    print('flask_cache testing...')
    return 'index page'


if __name__ == '__main__':
    app.run(debug=True)
