#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: AlphaFF
# @Date:   2018-08-04 17:20:07
# @Email: liushahedi@gmail.com
# @Last Modified by:   AlphaFF
# @Last Modified time: 2018-08-04 17:30:44

from gevent import monkey; monkey.patch_all()
import gevent
import socket
import time


def test1():
    print('test1')
    gevent.sleep()
    print('test111')


def test2():
    print('test2')
    gevent.sleep()
    print('test222')


# gevent.joinall([gevent.spawn(test1),
#                 gevent.spawn(test2)])

urls = ['www.baidu.com', 'www.gevent.com', 'www.python.org']
t1 = time.time()
jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]
gevent.joinall(jobs)
print([job.value for job in jobs])
t2 = time.time()
print(t2 - t1)
