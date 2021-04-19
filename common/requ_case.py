# -*- coding: utf-8 -*-

import json
from common.my_request import MyRequest


class ApiRequest(object):
    """
    接口请求封装后的使用模块
    调用类，传入url，请求方法，参数，请求headers，就可以进行请求，
    可以输出session，保留请求登录态，
    目前只支持dict格式的参数，和请求headers。
    """
    def __init__(self, url, method, params, headers, session=None):
        self.url = url
        self.method = method
        self.param = params
        self.headers = headers
        try:
            self.para_type = headers['Content-Type'].split('/')[1]
        except:
            self.para_type = ''
        if session is None:
            self.req = MyRequest()
        else:
            self.req = MyRequest(session)

    def test_api(self):
        if self.method.lower() == 'post':
            if self.para_type == 'json':
                res, spend = self.req.post(url=self.url, params=json.dumps(self.param), headers=self.headers)
            else:
                res, spend = self.req.post(url=self.url, params=self.param, headers=self.headers)
        elif self.method.lower() == 'get':
            res, spend = self.req.get(url=self.url, params=self.param, headers=self.headers)
        elif self.method.lower() == 'put':
            res, spend = self.req.put_file(url=self.url, params=self.param, headers=self.headers)
        elif self.method.lower() == 'delete':
            res, spend = self.req.del_file(url=self.url, params=self.param, headers=self.headers)
        else:
            res = {'请求方法错误': '不支持%s请求' % self.method}
            spend = -1
        return res, spend

    def get_session(self):
        return self.req.session
