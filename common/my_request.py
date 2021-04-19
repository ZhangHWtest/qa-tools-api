# -*- coding: utf-8 -*-

import requests
import json
from config import INTERFACE_TIME_OUT
from requests import exceptions


class MyRequest(object):
    """
    requests模块的简单的封装
    使用了session的请求方式，可以保留登录态
    """
    def __init__(self, session=None):
        if session is None:
            self.session = requests.session()
        else:
            self.session = session

    def get(self, url, params, headers):   # get消息
        spend = -1
        try:
            res = self.session.get(url, params=params, headers=headers, timeout=INTERFACE_TIME_OUT)
            spend = res.elapsed.total_seconds()
            if res.status_code != 200:
                return {'get请求出错': "响应状态码为 %d" % res.status_code}, spend
            res.encoding = 'UTF-8'
            json_response = json.loads(res.text)
            return json_response, spend
        except exceptions.Timeout:
            return {'get请求出错1': "请求超时"}, INTERFACE_TIME_OUT
        except exceptions.InvalidURL:
            return {'get请求出错2': "非法url"}, spend
        except exceptions.HTTPError:
            return {'get请求出错3': "http请求错误"}, spend
        except Exception as e:
            return {'get请求出错4': "错误原因:%s" % e}, spend

    def post(self, url, params, headers):   # post消息
        spend = -1
        try:
            res = self.session.post(url, headers=headers, data=params, timeout=INTERFACE_TIME_OUT)
            spend = res.elapsed.total_seconds()
            if res.status_code != 200:
                return {'post请求出错': "响应状态码为 %d" % res.status_code}, spend
            json_response = json.loads(res.text)
            return json_response, spend
        except exceptions.Timeout:
            return {'post请求出错1': "请求超时"}, INTERFACE_TIME_OUT
        except exceptions.InvalidURL:
            return {'post请求出错2': "非法url"}, spend
        except exceptions.HTTPError:
            return {'post请求出错3': "http请求错误"}, spend
        except Exception as e:
            return {'post请求出错4': "错误原因:%s" % e}, spend

    def del_file(self, url, params, headers):   # 删除的请求
        spend = -1
        try:
            res = self.session.delete(url, data=params, headers=headers, timeout=INTERFACE_TIME_OUT)
            spend = res.elapsed.total_seconds()
            if res.status_code != 200:
                return {'delete请求出错': "响应状态码为 %d" % res.status_code}, spend
            json_response = json.loads(res.text)
            return json_response, spend
        except exceptions.Timeout:
            return {'delete请求出错1': "请求超时"}, INTERFACE_TIME_OUT
        except exceptions.InvalidURL:
            return {'delete请求出错2': "非法url"}, spend
        except exceptions.HTTPError:
            return {'delete请求出错3': "http请求错误"}, spend
        except Exception as e:
            return {'delete请求出错4': "错误原因:%s" % e}, spend

    def put_file(self, url, params, headers):   # put请求
        spend = -1
        try:
            data = json.dumps(params)
            res = self.session.put(url, data, headers=headers, timeout=INTERFACE_TIME_OUT)
            spend = res.elapsed.total_seconds()
            if res.status_code != 200:
                return {'put请求出错': "响应状态码为 %d" % res.status_code}, spend
            json_response = json.loads(res.text)
            return json_response, spend
        except exceptions.Timeout:
            return {'put请求出错1': "请求超时"}, INTERFACE_TIME_OUT
        except exceptions.InvalidURL:
            return {'put请求出错2': "非法url"}, spend
        except exceptions.HTTPError:
            return {'put请求出错3': "http请求错误"}, spend
        except Exception as e:
            return {'put请求出错4': "错误原因:%s" % e}, spend
