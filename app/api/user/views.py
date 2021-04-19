# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request, session
from flask.views import MethodView
from flask_login import login_required, current_user
from app import loginManager, cache
from app.models import *
from .my_schema import *
from common.response import ResMsg
from common.response_message import *
from common.return_list_page import list_page
from common.json_checker import format_checker

user = Blueprint('user', __name__)


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UserList(MethodView):
    """用户列表"""
    @login_required
    # @cache.cached(timeout=10, key_prefix='view_%s')
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(user_list_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        page_num = data.get('page_num')
        page_size = data.get('page_size', 10)
        user_list = list()
        if not page_num:
            res.update(code=-1, data='', msg=param_error)
            return jsonify(res.data)
        try:
            users = User.query.all()
        except Exception as e:
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)
        if users:
            for u in users:
                status = 1 if u.status else 0
                user_info = {
                    'uid': u.id,
                    'username': u.username,
                    'role': u.roles.name,
                    'status': status,
                }
                user_list.append(user_info)
        data, total = list_page(user_list, page_size, page_num)
        res.update(code=1, data=data, msg=request_success)
        res.add_field(name='page_total_num', value=total)
        return jsonify(res.data)


class AddUser(MethodView):
    """管理员新增用户"""
    @login_required
    def post(self):
        res = ResMsg()
        if session.get('role') != 3:
            res.update(code=-4, data='', msg=permission_denied)
            return jsonify(res.data)
        data = request.get_json()
        flag, mes = format_checker(add_user_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        username = data.get('username')
        user_email = data.get('email')
        exist_user = User.query.filter_by(username=username).first()
        if exist_user:
            res.update(code=-1, data='', msg=user_exist)
            return jsonify(res.data)
        email = User.query.filter_by(user_email=user_email).first()
        if email:
            res.update(code=-1, data='', msg=email_exist)
            return jsonify(res.data)
        new_user = User(username=username, user_email=user_email, role_id=1)
        new_user.set_password('111111')   # 管理员创建用户默认密码 111111，默认角色 用户
        db.session.add(new_user)
        user_info = {'user': username, 'user_role': 'User'}
        try:
            db.session.commit()
            res.update(code=1, data=user_info, msg=add_user_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=add_user_failure)
            return jsonify(res.data)


class ChangePassword(MethodView):
    """变更密码"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(change_pass_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        password = data.get('password')
        set_password = data.get('set_password')
        if password != set_password:
            res.update(code=-1, data='', msg=password_not_same)
            return jsonify(res.data)
        users = User.query.filter_by(id=current_user.id).first()
        users.set_password(password)
        try:
            db.session.commit()
            res.update(code=1, data='', msg=change_password_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=change_password_failure)
            return jsonify(res.data)


class ResetPassword(MethodView):
    """管理员重置密码为111111"""
    @login_required
    def post(self):
        res = ResMsg()
        if session.get('role') != 3:
            res.update(code=-4, data='', msg=permission_denied)
            return jsonify(res.data)
        data = request.get_json()
        flag, mes = format_checker(reset_pass_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        uid = data.get('uid')
        exist_user = User.query.filter_by(id=uid).first()
        if not exist_user:
            res.update(code=-1, data='', msg=user_not_exist)
            return jsonify(res.data)
        exist_user.set_password('111111')
        try:
            db.session.commit()
            res.update(code=1, data='', msg=reset_password_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=reset_password_failure)
            return jsonify(res.data)


class OnOffUser(MethodView):
    """管理员禁用用户"""
    @login_required
    def post(self):
        res = ResMsg()
        if session.get('role') != 3:
            res.update(code=-4, data='', msg=permission_denied)
            return jsonify(res.data)
        data = request.get_json()
        flag, mes = format_checker(onoff_user_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        uid = data.get('uid')
        status = data.get('status')
        exist_user = User.query.filter_by(id=uid).first()
        if not exist_user:
            res.update(code=-1, data='', msg=user_not_exist)
            return jsonify(res.data)
        if exist_user.id == current_user.id:
            res.update(code=-1, data='', msg=cannot_onoff_self)
            return jsonify(res.data)
        if status == 1:
            exist_user.status = True
        elif status == 0:
            exist_user.status = False
        else:
            res.update(code=-1, data='', msg=param_error)
            return jsonify(res.data)
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class SetRole(MethodView):
    """设置用户角色"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(set_role_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        uid = data.get('uid')
        role_id = data.get('role_id')
        exist_user = User.query.filter_by(id=uid).first()
        if not exist_user:
            res.update(code=-1, data='', msg=user_not_exist)
            return jsonify(res.data)
        if session.get('role') == 3:
            pass
        elif session.get('role') == 2 and exist_user.role_id != 3 and role_id != 3:
            pass
        else:
            res.update(code=-4, data='', msg=permission_denied)
            return jsonify(res.data)
        exist_user.role_id = role_id
        try:
            db.session.commit()
            res.update(code=1, data='', msg=set_role_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=set_role_failure)
            return jsonify(res.data)
