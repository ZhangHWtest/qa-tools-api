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

model = Blueprint('model', __name__)


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class ModelList(MethodView):
    """模块列表"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(model_list_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        project_id = data.get('project_id')
        page_num = data.get('page_num')
        page_size = data.get('page_size', 10)
        model_list = list()
        try:
            models = Model.query.filter_by(project_id=project_id, status=True).order_by(Model.id.desc()).all()
        except Exception as e:
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)
        if models:
            for m in models:
                model_info = {
                    'model_id': m.id,
                    'model_name': m.model_name,
                    'create_user': m.users.username,
                }
                model_list.append(model_info)
        data, total = list_page(model_list, page_size, page_num)
        res.update(code=1, data=data, msg=request_success)
        res.add_field(name='page_total_num', value=total)
        return jsonify(res.data)


class ModelInfo(MethodView):
    """模块信息"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(model_info_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        model_id = data.get('model_id')
        exist_model = Model.query.filter_by(id=model_id, status=True).first()
        if not exist_model:
            res.update(code=-1, data='', msg=model_not_exist_error)
            return jsonify(res.data)
        project_name = exist_model.projects.project_name if exist_model.project_id else ''
        model_info = {
            'model_id': exist_model.id,
            'model_name': exist_model.model_name,
            'project_name': project_name,
            'create_user': exist_model.users.username,
        }
        res.update(code=1, data=model_info, msg=request_success)
        return jsonify(res.data)


class AddModel(MethodView):
    """新增模块"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(add_model_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        project_id = data.get('project_id')
        model_name = data.get('model_name')
        model_desc = data.get('model_desc')
        exist_project = Project.query.filter_by(id=project_id, status=True).first()
        if not exist_project:
            res.update(code=-1, data='', msg=project_not_exist_error)
            return jsonify(res.data)
        model_desc = model_desc if model_desc else ''
        new_model = Model(
            model_name=model_name,
            model_desc=model_desc,
            project_id=project_id,
            c_uid=current_user.id
        )
        db.session.add(new_model)
        try:
            db.session.commit()
            model_info = {
                'model_id': new_model.id,
                'model_name': model_name,
                'create_user': current_user.id,
            }
            res.update(code=1, data=model_info, msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class EditModel(MethodView):
    """编辑模块"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(add_model_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        model_id = data.get('model_id')
        model_name = data.get('model_name')
        model_desc = data.get('model_desc')
        exist_model = Model.query.filter_by(id=model_id, status=True).first()
        if not exist_model:
            res.update(code=-1, data='', msg=model_not_exist_error)
            return jsonify(res.data)
        model_desc = model_desc if model_desc else ''
        exist_model.model_name = model_name
        exist_model.model_desc = model_desc
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class DelModel(MethodView):
    """删除模块"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(del_model_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        model_id = data.get('model_id')
        exist_model = Model.query.filter_by(id=model_id, status=True).first()
        if not exist_model:
            res.update(code=-1, data='', msg=model_not_exist_error)
            return jsonify(res.data)
        exist_model.status = False
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)
