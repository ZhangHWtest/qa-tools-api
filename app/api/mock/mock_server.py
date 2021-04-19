"""
mock server封装,用于在提供mock服务的时候使用
"""
import json
from flask import request, jsonify
from app.models import *
from common.response import ResMsg
from common.response_message import *

res = ResMsg()


def get_mock_data(path):
    exist_mock = Mock.query.filter_by(path=path, status=True).first()
    if not exist_mock:
        res.update(code=-1, data='', msg=mock_not_exist_error)
        return jsonify(res.data)
    if exist_mock.run_status == 0:
        res.update(code=-1, data='', msg=mock_close_error)
        return jsonify(res.data)
    method = request.method
    if method.lower() != exist_mock.method:
        e = {'mock_method': exist_mock.method, 'req_method': method}
        res.update(code=-1, data=e, msg=mock_method_error)
        return jsonify(res.data)
    if exist_mock.check_header == 1:
        header = json.loads(exist_mock.header)
        headers = request.headers
        if not header == headers:
            e = {'mock_header': header, 'req_header': headers}
            res.update(code=-1, data=e, msg=mock_header_check_error)
            return jsonify(res.data)
    if exist_mock.check_params == 1:
        params = json.loads(exist_mock.params)
        if method == "GET":
            param = request.values.to_dict()
        elif method == "POST":
            param = request.get_json()
        else:
            param = 'null'
        if not params == param:
            e = {'mock_params': params, 'req_params': param}
            res.update(code=-1, data=e, msg=mock_params_check_error)
            return jsonify(res.data)
    result = json.loads(exist_mock.response)
    res.update(code=1, data=result, msg=request_success)
    return jsonify(res.data)
