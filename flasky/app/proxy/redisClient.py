#!/usr/bin/env python
# coding=utf-8

import redis
import random


class RedisClient(object):
    # 数据库的连接
    def __init__(self, name, host, port, passwd):
        self.name = name
        self.__conn = redis.Redis(host=host, port=port, db=1, password=passwd)

    # 向数据库中插入数据
    def put(self, key):
        return self.__conn.hincrby(self.name, key, 1)
        pass

    # 随机获得数据库中的一条数据
    def get(self):
        result = self.__conn.hgetall(self.name)
        return random.choice(list(result.keys())).decode('utf-8') if result else None

    # 获得一条数据的key的value值
    def get_value(self, key):
        value = self.__conn.hget(self.name, key)
        return value if value else None
        pass

    # pop一条数据,并删除
    def pop(self):
        key = self.get()
        if key:
            self.__conn.hdel(self.name, key)
        return key
        pass

    # 删除某条数据
    def delete(self, key):
        self.__conn.hdel(self.name, key)
        pass

    # 记数
    def inckey(self, key, value):
        self.__conn.hincrby(self.name, key, value)
        pass

    # 获得所有的keys
    def get_all(self):
        return [key.decode('utf-8') for key in self.__conn.hgetall(self.name).keys()]
        pass

    # 获得当前表的数据长度，即数据总量
    def get_length(self):
        return self.__conn.hlen(self.name)
        pass

    # 换表
    def change_table(self, name):
        self.name = name
        pass


if __name__ == "__main__":
    redis_conn = RedisClient('proxy', 'localhost', 6379, 'redis')
    key = '10.1.1.3:3234'
    redis_conn.put(key)
    proxy = redis_conn.get()
    print(proxy)
    # value = redis_conn.get_value(key)
    # print(value)
    # key = redis_conn.pop()
    # print(key)
    # redis_conn.delete(key)
    length = redis_conn.get_length()
    print(length)
    all = redis_conn.get_all()
    print(list(all))
