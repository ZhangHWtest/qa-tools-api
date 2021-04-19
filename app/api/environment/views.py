# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_login import login_required, current_user
from app import loginManager
from app.models import *
from .my_schema import *
from common.response import ResMsg
from common.response_message import *
from common.return_list_page import list_page
from common.json_checker import format_checker

environment = Blueprint('environment', __name__)


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class EnvironmentList(MethodView):
    """环境列表"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(env_list_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        page_num = data.get('page_num')
        page_size = data.get('page_size', 10)
        env_list = list()
        try:
            environments = Environment.query.filter_by(status=True).order_by(Environment.id.desc()).all()
        except Exception as e:
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)
        if environments:
            for env in environments:
                env_info = {
                    'env_id': env.id,
                    'env_name': env.env_name,
                    'url': env.url,
                    'create_user': env.users.username,
                }
                env_list.append(env_info)
        data, total = list_page(env_list, page_size, page_num)
        res.update(code=1, data=data, msg=request_success)
        res.add_field(name='page_total_num', value=total)
        return jsonify(res.data)


class EnvironmentInfo(MethodView):
    """环境信息"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(env_info_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        env_id = data.get('env_id')
        exist_env = Environment.query.filter_by(id=env_id, status=True).first()
        if not exist_env:
            res.update(code=-1, data='', msg=env_not_exist_error)
            return jsonify(res.data)
        use_db = 1 if exist_env.use_db else 0
        env_info = {
            'env_id': exist_env.id,
            'env_name': exist_env.env_name,
            'desc': exist_env.desc,
            'url': exist_env.url,
            'use_db': use_db,
            'db_host': exist_env.db_host,
            'db_port': exist_env.db_port,
            'db_user': exist_env.db_user,
            'db_pass': exist_env.db_pass,
            'database': exist_env.database,
            'create_user': exist_env.users.username,
        }
        res.update(code=1, data=env_info, msg=request_success)
        return jsonify(res.data)


class AddEnvironment(MethodView):
    """新增环境"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(add_env_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        env_name = data.get('env_name')
        desc = data.get('desc')
        url = data.get('url')
        use_db = data.get('use_db')
        db_host = data.get('db_host')
        db_port = data.get('db_port')
        db_user = data.get('db_user')
        db_pass = data.get('db_pass')
        database = data.get('database')
        desc = desc if desc else ''
        use_db = True if use_db == 1 else False
        db_host = db_host if db_host else ''
        db_port = db_port if db_port else ''
        db_user = db_user if db_user else ''
        db_pass = db_pass if db_pass else ''
        database = database if database else ''
        if use_db:
            if db_host and db_port and db_user and db_pass and database:
                pass
            else:
                res.update(code=-1, data='', msg=db_info_empty_error)
                return jsonify(res.data)
        else:
            db_host = db_port = db_user = db_pass = database = ''
        new_env = Environment(
            env_name=env_name,
            desc=desc,
            url=url,
            use_db=use_db,
            db_host=db_host,
            db_port=db_port,
            db_user=db_user,
            db_pass=db_pass,
            database=database,
            c_uid=current_user.id
        )
        db.session.add(new_env)
        try:
            db.session.commit()
            env_info = {
                'env_id': new_env.id,
                'env_name': env_name,
            }
            res.update(code=1, data=env_info, msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class EditEnvironment(MethodView):
    """编辑环境"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(edit_env_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        env_id = data.get('env_id')
        env_name = data.get('env_name')
        desc = data.get('desc')
        url = data.get('url')
        use_db = data.get('use_db')
        db_host = data.get('db_host')
        db_port = data.get('db_port')
        db_user = data.get('db_user')
        db_pass = data.get('db_pass')
        database = data.get('database')
        desc = desc if desc else ''
        use_db = True if use_db == 1 else False
        db_host = db_host if db_host else ''
        db_port = db_port if db_port else ''
        db_user = db_user if db_user else ''
        db_pass = db_pass if db_pass else ''
        database = database if database else ''
        if use_db:
            if db_host and db_port and db_user and db_pass and database:
                pass
            else:
                res.update(code=-1, data='', msg=db_info_empty_error)
                return jsonify(res.data)
        else:
            db_host = db_port = db_user = db_pass = database = ''
        exist_env = Environment.query.filter_by(id=env_id, status=True).first()
        if not exist_env:
            res.update(code=-1, data='', msg=env_not_exist_error)
            return jsonify(res.data)
        exist_env.env_name = env_name
        exist_env.desc = desc
        exist_env.url = url
        exist_env.use_db = use_db
        exist_env.db_host = db_host
        exist_env.db_port = db_port
        exist_env.db_user = db_user
        exist_env.db_pass = db_pass
        exist_env.database = database
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class DelEnvironment(MethodView):
    """删除环境"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(del_env_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        env_id = data.get('env_id')
        exist_env = Environment.query.filter_by(id=env_id, status=True).first()
        if not exist_env:
            res.update(code=-1, data='', msg=env_not_exist_error)
            return jsonify(res.data)
        exist_env.status = False
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)
