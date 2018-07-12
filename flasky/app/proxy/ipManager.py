#!/usr/bin python3
# coding:utf-8

from .getter import ProxyGetter
from .redisClient import RedisClient


class ProxyManager(object):
    def __init__(self):
        self.db = RedisClient('proxy', '121.40.184.36', 6379, 'redis')
        self.raw_proxy = 'raw'
        self.useful_proxy = 'useful'
        pass

    # 将代理添加到数据库中
    def refresh(self):
        proxy_set = set()
        p = ProxyGetter()
        for proxy in p.run():
            proxy_set.add(proxy)
        self.db.change_table(self.raw_proxy)
        print(proxy_set)
        for proxy in proxy_set:
            self.db.put(proxy)

        pass

    # 获得一个有用的代理
    def get(self):
        self.db.change_table(self.useful_proxy)
        return self.db.get()
        pass

    # 从数据库中删除一个代理
    def delete(self, proxy):
        self.db.change_table(self.useful_proxy)
        self.db.delete(proxy)
        pass

    # 获得所有代理
    def getAll(self):
        self.db.change_table(self.useful_proxy)
        return self.db.get_all()
        pass

    # 获取数据库的数据量
    def get_status(self):
        self.db.change_table(self.raw_proxy)
        total_raw_proxy = self.db.get_length()
        self.db.change_table(self.useful_proxy)
        total_useful_proxy = self.db.get_length()
        return {"total_raw_proxy": total_raw_proxy, "total_userful_proxy": total_useful_proxy}


if __name__ == '__main__':
    pp = ProxyManager()
    pp.refresh()
    # print(pp.get_status())
