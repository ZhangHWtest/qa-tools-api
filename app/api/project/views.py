# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request, session
from flask.views import MethodView
from flask_login import login_required, current_user
from app import loginManager
from app.models import *
from .my_schema import *
from common.response import ResMsg
from common.response_message import *
from common.return_list_page import list_page
from common.json_checker import format_checker

project = Blueprint('project', __name__)


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class ProjectList(MethodView):
    """项目列表"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(pro_list_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        project_name = data.get('project_name')
        page_num = data.get('page_num')
        page_size = data.get('page_size', 10)
        project_list = list()
        try:
            projects = Project.query.filter_by(status=True).order_by(Project.id.desc()).all()
        except Exception as e:
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)
        if projects:
            for p in projects:
                if project_name:
                    if project_name in p.project_name:
                        project_info = {
                            'project_id': p.id,
                            'project_name': p.project_name,
                            'create_user': p.users.username,
                        }
                        project_list.append(project_info)
                else:
                    project_info = {
                        'project_id': p.id,
                        'project_name': p.project_name,
                        'create_user': p.users.username,
                    }
                    project_list.append(project_info)
        data, total = list_page(project_list, page_size, page_num)
        res.update(code=1, data=data, msg=request_success)
        res.add_field(name='page_total_num', value=total)
        return jsonify(res.data)


class ProjectInfo(MethodView):
    """项目信息"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(pro_info_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        project_id = data.get('project_id')
        exist_project = Project.query.filter_by(id=project_id, status=True).first()
        if not exist_project:
            res.update(code=-1, data='', msg=project_not_exist_error)
            return jsonify(res.data)
        project_info = {
            'project_id': exist_project.id,
            'project_name': exist_project.project_name,
            'create_user': exist_project.users.username,
        }
        res.update(code=1, data=project_info, msg=request_success)
        return jsonify(res.data)


class AddProject(MethodView):
    """管理员新增项目"""
    @login_required
    def post(self):
        res = ResMsg()
        if session.get('role') != 3:
            res.update(code=-4, data='', msg=permission_denied)
            return jsonify(res.data)
        data = request.get_json()
        flag, mes = format_checker(add_pro_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        project_name = data.get('project_name')
        project_desc = data.get('project_desc')
        exist_project = Project.query.filter_by(project_name=project_name, status=True).first()
        if exist_project:
            res.update(code=-1, data='', msg=name_exist_error)
            return jsonify(res.data)
        project_desc = project_desc if project_desc else ''
        new_project = Project(project_name=project_name, project_desc=project_desc, c_uid=current_user.id)
        db.session.add(new_project)
        try:
            db.session.commit()
            project_info = {
                'project_id': new_project.id,
                'project_name': project_name,
                'create_user': current_user.id,
            }
            res.update(code=1, data=project_info, msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class EditProject(MethodView):
    """管理员编辑项目"""
    @login_required
    def post(self):
        res = ResMsg()
        if session.get('role') != 3:
            res.update(code=-4, data='', msg=permission_denied)
            return jsonify(res.data)
        data = request.get_json()
        flag, mes = format_checker(edit_pro_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        project_id = data.get('project_id')
        project_name = data.get('project_name')
        project_desc = data.get('project_desc')
        exist_project = Project.query.filter_by(id=project_id, status=True).first()
        if not exist_project:
            res.update(code=-1, data='', msg=project_not_exist_error)
            return jsonify(res.data)
        filters = {
            Project.id != project_id,
            Project.project_name == project_name,
            Project.status == True,  # 这里必须用==
        }
        same_project = Project.query.filter(*filters).first()
        if same_project:  # 项目名称排重
            res.update(code=-1, data='', msg=name_exist_error)
            return jsonify(res.data)
        project_desc = project_desc if project_desc else ''
        exist_project.project_name = project_name
        exist_project.project_desc = project_desc
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class DelProject(MethodView):
    """管理员删除项目"""
    @login_required
    def post(self):
        res = ResMsg()
        if session.get('role') != 3:
            res.update(code=-4, data='', msg=permission_denied)
            return jsonify(res.data)
        data = request.get_json()
        flag, mes = format_checker(del_pro_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        project_id = data.get('project_id')
        exist_project = Project.query.filter_by(id=project_id, status=True).first()
        if not exist_project:
            res.update(code=-1, data='', msg=project_not_exist_error)
            return jsonify(res.data)
        exist_project.status = False
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)
