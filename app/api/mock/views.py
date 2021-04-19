# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_login import login_required, current_user
from app import loginManager
from app.models import *
from .my_schema import *
from .mock_server import get_mock_data
from common.response import ResMsg
from common.response_message import *
from common.return_list_page import list_page
from common.json_checker import format_checker, is_json

mock = Blueprint('mock', __name__)


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class MockList(MethodView):
    """mock列表"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(mock_list_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        page_num = data.get('page_num')
        page_size = data.get('page_size', 10)
        mock_list = list()
        try:
            mocks = Mock.query.filter_by(status=True).order_by(Mock.id.desc()).all()
        except Exception as e:
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)
        if mocks:
            for mo in mocks:
                mock_info = {
                    'mock_id': mo.id,
                    'mock_name': mo.mock_name,
                    'path': mo.path,
                    'run_status': mo.run_status,
                    'create_user': mo.users.username,
                }
                mock_list.append(mock_info)
        data, total = list_page(mock_list, page_size, page_num)
        res.update(code=1, data=data, msg=request_success)
        res.add_field(name='page_total_num', value=total)
        return jsonify(res.data)


class MockInfo(MethodView):
    """mock信息"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(mock_info_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        mock_id = data.get('mock_id')
        exist_mock = Mock.query.filter_by(id=mock_id, status=True).first()
        if not exist_mock:
            res.update(code=-1, data='', msg=mock_not_exist_error)
            return jsonify(res.data)
        mock_info = {
            'mock_id': exist_mock.id,
            'mock_name': exist_mock.mock_name,
            'mock_desc': exist_mock.mock_desc,
            'method': exist_mock.method,
            'path': exist_mock.path,
            'params': exist_mock.params,
            'header': exist_mock.header,
            'response': exist_mock.response,
            'res_type': exist_mock.res_type,
            'update_time': exist_mock.update_time,
            'run_status': exist_mock.run_status,
            'check_params': exist_mock.check_params,
            'check_header': exist_mock.check_header,
            'create_user': exist_mock.users.username,
        }
        res.update(code=1, data=mock_info, msg=request_success)
        return jsonify(res.data)


class AddMock(MethodView):
    """新增mock"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(add_mock_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        mock_name = data.get('mock_name')
        mock_desc = data.get('mock_desc')
        method = data.get('method')
        path = data.get('path')
        params = data.get('params')
        header = data.get('header')
        response = data.get('response')
        res_type = data.get('res_type')
        check_params = data.get('check_params')
        check_header = data.get('check_header')
        if check_params == 1:
            if not params:
                res.update(code=-1, data='', msg=mock_params_empty_error)
                return jsonify(res.data)
            if not is_json(params):
                res.update(code=-1, data=params, msg=param_not_json_error)
                return jsonify(res.data)
        if check_header == 1:
            if not header:
                res.update(code=-1, data='', msg=mock_params_empty_error)
                return jsonify(res.data)
            if not is_json(header):
                res.update(code=-1, data=header, msg=param_not_json_error)
                return jsonify(res.data)
        if not is_json(response):
            res.update(code=-1, data=response, msg=param_not_json_error)
            return jsonify(res.data)
        if res_type != 'json':
            res.update(code=-1, data=res_type, msg=mock_resp_type_error)
            return jsonify(res.data)
        exist_mock = Mock.query.filter_by(path=path, status=True).first()
        if exist_mock:
            res.update(code=-1, data=path, msg=path_exist_error)
            return jsonify(res.data)
        new_mock = Mock(
            mock_name=mock_name,
            mock_desc=mock_desc if mock_desc else '',
            method=method,
            path=path,
            params=params if params else '',
            header=header if header else '',
            response=response,
            res_type=res_type,
            update_time=datetime.datetime.now(),
            check_params=check_params,
            check_header=check_header,
            c_uid=current_user.id
        )
        db.session.add(new_mock)
        try:
            db.session.commit()
            mock_info = {
                'mock_id': new_mock.id,
                'mock_name': mock_name,
            }
            res.update(code=1, data=mock_info, msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class EditMock(MethodView):
    """编辑mock"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(edit_mock_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        mock_id = data.get('mock_id')
        mock_name = data.get('mock_name')
        mock_desc = data.get('mock_desc')
        method = data.get('method')
        path = data.get('path')
        params = data.get('params')
        header = data.get('header')
        response = data.get('response')
        res_type = data.get('res_type')
        check_params = data.get('check_params')
        check_header = data.get('check_header')
        exist_mock = Mock.query.filter_by(id=mock_id, status=True).first()
        if not exist_mock:
            res.update(code=-1, data='', msg=mock_not_exist_error)
            return jsonify(res.data)
        other_mock = Mock.query.filter_by(path=path, status=True).first()
        if other_mock and other_mock.id != mock_id:
            res.update(code=-1, data='', msg=path_exist_error)
            return jsonify(res.data)
        if check_params == 1:
            if not params:
                res.update(code=-1, data='', msg=mock_params_empty_error)
                return jsonify(res.data)
            if not is_json(params):
                res.update(code=-1, data=params, msg=param_not_json_error)
                return jsonify(res.data)
        if check_header == 1:
            if not header:
                res.update(code=-1, data='', msg=mock_params_empty_error)
                return jsonify(res.data)
            if not is_json(header):
                res.update(code=-1, data=header, msg=param_not_json_error)
                return jsonify(res.data)
        if not is_json(response):
            res.update(code=-1, data=response, msg=param_not_json_error)
            return jsonify(res.data)
        exist_mock.mock_name = mock_name
        exist_mock.mock_desc = mock_desc if mock_desc else ''
        exist_mock.method = method
        exist_mock.path = path
        exist_mock.params = params if params else ''
        exist_mock.header = header if header else ''
        exist_mock.response = response
        exist_mock.res_type = res_type
        exist_mock.update_time = datetime.datetime.now()
        exist_mock.check_params = check_params
        exist_mock.check_header = check_header
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class DelMock(MethodView):
    """删除mock"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(del_mock_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        mock_id = data.get('mock_id')
        exist_mock = Mock.query.filter_by(id=mock_id, status=True).first()
        if not exist_mock:
            res.update(code=-1, data='', msg=mock_not_exist_error)
            return jsonify(res.data)
        if exist_mock.run_status == 1:
            res.update(code=-1, data='', msg=mock_running_error)
            return jsonify(res.data)
        exist_mock.status = False
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class MockStatus(MethodView):
    """开启/关闭mock"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(mock_info_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        mock_id = data.get('mock_id')
        exist_mock = Mock.query.filter_by(id=mock_id, status=True).first()
        if not exist_mock:
            res.update(code=-1, data='', msg=mock_not_exist_error)
            return jsonify(res.data)
        if exist_mock.run_status == 0:
            exist_mock.run_status = 1
        else:
            exist_mock.run_status = 0
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class MockServer(MethodView):
    """mock服务"""
    def get(self, path):    # get请求方法
        data = get_mock_data(path)
        return data

    def post(self, path):   # post请求方法
        data = get_mock_data(path)
        return data
