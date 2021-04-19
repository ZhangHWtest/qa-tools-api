#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
from config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD, MAX_CONNEC_REDIS


class MyRedis(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB):
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        try:
            pool = redis.ConnectionPool(host=self.host, port=self.port, password=self.password, db=self.db,
                                        decode_responses=True, max_connections=MAX_CONNEC_REDIS)
            self.conn = redis.Redis(connection_pool=pool)
            print("redis连接成功")
        except Exception as e:
            print("redis连接失败，异常：%s" % str(e))

    def set_value(self, key, value, time=None):
        return self.conn.set(name=key, value=value, ex=time)

    def get_value(self, key):
        return self.conn.get(key)

    def del_value(self, key):
        return self.conn.delete(key)

    def check_redis_lock(self, key, value, time):
        """redis添加键值对成功，则返回True，已存在键值添加失败，则返回None"""
        return self.conn.set(name=key, value=value, ex=time, nx=True)


if __name__ == '__main__':
    r = MyRedis()
    k, v = ('xxx', 'yyy')
    # r.set_value(k, v, 100)
    res = r.get_value(k)
    print(res)
    # r.del_value(k)
    print(r.check_redis_lock(k, v, 10))
