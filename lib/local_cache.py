#!/usr/bin/env python
# -*- coding: utf-8 -*-

import weakref
import collections
import time
import json
from functools import wraps


class LocalCache():
    notFound = object()

    # list dict等不支持弱引用，但其子类支持，故这里包装了下
    class Dict(dict):
        def __del__(self):
            pass

    def __init__(self, maxlen=5):
        self.weak = weakref.WeakValueDictionary()
        self.strong = collections.deque(maxlen=maxlen)

    @staticmethod
    def now_time():
        return int(time.time())

    def get(self, key):
        value = self.weak.get(key, self.notFound)
        if value is not self.notFound:
            expire = value[r'expire']
            if self.now_time() > expire:
                return self.notFound
            else:
                return value
        else:
            return self.notFound

    def set(self, key, value):
        # strongRef作为强引用避免被回收
        self.weak[key] = strongRef = LocalCache.Dict(value)
        # 放入定长队列，弹出元素马上被回收
        self.strong.append(strongRef)


# 装饰器
def func_cache(expire=0):
    caches = LocalCache()
    def _wrappend(func):
        @wraps(func)
        def __wrapped(*args, **kwargs):
            # 计算出缓存的key值
            # key = str(func) + str(args) + str(kwargs)
            key = str(func.__name__)
            value = caches.get(key)
            if value is LocalCache.notFound:
                result = func(*args, **kwargs)
                caches.set(key, {r'result': result, r'expire': expire + caches.now_time()})
                result = caches.get(key)[r'result']
            else:
                result = value[r'result']
            return result
        return __wrapped
    return _wrappend


if __name__ == '__main__':
    # 测试函数
    @func_cache(expire=300)
    def test_cache(v):
        # 模拟任务处理时常3秒
        time.sleep(3)
        k = 'key'
        print('work 3s')
        return json.dumps({k: v})


    print(test_cache(1))
    print(test_cache(2))

    print(test_cache(1))
    print(test_cache(2))

