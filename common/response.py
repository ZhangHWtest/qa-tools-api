# -*- coding: utf-8 -*-


class ResMsg(object):
    """
    封装响应文本
    """

    def __init__(self, code=0, msg='', data=None):
        self._msg = msg
        self._code = code
        self._data = data

    def update(self, code=None, msg=None, data=None):
        """
        更新默认响应文本
        :param code: 响应状态码
        :param data: 响应数据
        :param msg: 响应消息
        :return:
        """
        if code is not None:
            self._code = code
        if data is not None:
            self._data = data
        if msg is not None:
            self._msg = msg

    def add_field(self, name=None, value=None):
        """
        在响应文本中加入新的字段，方便使用
        :param name: 变量名
        :param value: 变量值
        :return:
        """
        if name is not None and value is not None:
            self.__dict__[name] = value

    @property
    def data(self):
        """
        输出响应文本内容
        :return:
        """
        body = self.__dict__
        body["code"] = body.pop("_code")
        body["msg"] = body.pop("_msg")
        body["data"] = body.pop("_data")
        return body
