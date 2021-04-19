# -*- coding: utf-8 -*-

import json
from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_login import login_required, current_user
from app import loginManager
from app.models import *
from .my_schema import *
from .import_json import ImportJson
from common.response import ResMsg
from common.response_message import *
from common.return_list_page import list_page
from common.json_checker import format_checker, is_json

interface = Blueprint('interface', __name__)


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class InterfaceList(MethodView):
    """
    接口列表
    model_id, project_id都是非必填参数
    优先获取model下的接口，然后才是project下的接口
    都没有时，获取全部接口
    """
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(interface_list_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        project_id = data.get('project_id')
        model_id = data.get('model_id')
        interface_name = data.get('interface_name') if data.get('interface_name') is not None else ''
        page_num = data.get('page_num')
        page_size = data.get('page_size', 10)
        interface_list = list()
        if model_id:
            try:
                interfaces = Interface.query.filter_by(model_id=model_id, status=True).filter(
                    Interface.Interface_name.like('%' + interface_name + '%')
                ).order_by(Interface.id.desc()).all()
            except Exception as e:
                res.update(code=-1, data=str(e), msg=request_fail)
                return jsonify(res.data)
        elif project_id:
            try:
                interfaces = Interface.query.filter_by(project_id=project_id, status=True).filter(
                    Interface.Interface_name.like('%' + interface_name + '%')
                ).order_by(Interface.id.desc()).all()
            except Exception as e:
                res.update(code=-1, data=str(e), msg=request_fail)
                return jsonify(res.data)
        else:
            try:
                interfaces = Interface.query.filter_by(status=True).filter(
                    Interface.Interface_name.like('%' + interface_name + '%')
                ).order_by(Interface.id.desc()).all()
            except Exception as e:
                res.update(code=-1, data=str(e), msg=request_fail)
                return jsonify(res.data)
        if interfaces:
            for i in interfaces:
                project_name = i.projects.project_name if i.project_id else ''
                model_name = i.models.model_name if i.model_id else ''
                interface_info = {
                    'interface_id': i.id,
                    'interface_name': i.Interface_name,
                    'interface_type': i.interface_type,
                    'method': i.method,
                    'path': i.path,
                    'project_name': project_name,
                    'model_name': model_name,
                    'create_user': i.users.username,
                }
                interface_list.append(interface_info)
        data, total = list_page(interface_list, page_size, page_num)
        res.update(code=1, data=data, msg=request_success)
        res.add_field(name='page_total_num', value=total)
        return jsonify(res.data)


class InterfaceInfo(MethodView):
    """接口信息"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(interface_info_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        interface_id = data.get('interface_id')
        exist_interface = Interface.query.filter_by(id=interface_id, status=True).first()
        if not exist_interface:
            res.update(code=-1, data='', msg=interface_not_exist_error)
            return jsonify(res.data)
        project_name = exist_interface.projects.project_name if exist_interface.project_id else ''
        model_name = exist_interface.models.model_name if exist_interface.model_id else ''
        params = Parameter.query.filter_by(interface_id=interface_id, status=True).all()
        param_list = list()
        if params:
            for p in params:
                is_necessary = 1 if p.necessary else 0
                param_info = {
                    'param_id': p.id,
                    'param_name': p.param_name,
                    'param_desc': p.param_desc,
                    'is_necessary': is_necessary,
                    'default': p.default,
                }
                param_list.append(param_info)
        header = json.loads(exist_interface.header) if exist_interface.header else {}
        response = exist_interface.response if exist_interface.response else ''
        interface_info = {
            'interface_id': exist_interface.id,
            'interface_name': exist_interface.Interface_name,
            'interface_desc': exist_interface.Interface_desc,
            'interface_type': exist_interface.interface_type,
            'method': exist_interface.method,
            'path': exist_interface.path,
            'header': header,
            'params': param_list,
            'response': response,
            'project_name': project_name,
            'model_name': model_name,
            'create_user': exist_interface.users.username,
        }
        res.update(code=1, data=interface_info, msg=request_success)
        return jsonify(res.data)


class AddInterface(MethodView):
    """新增接口"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(add_interface_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        project_id = data.get('project_id')
        model_id = data.get('model_id')
        interface_name = data.get('interface_name')
        interface_desc = data.get('interface_desc')
        interface_type = data.get('interface_type')
        method = data.get('method')
        path = data.get('path')
        exist_project = Project.query.filter_by(id=project_id, status=True).first()
        if not exist_project:
            res.update(code=-1, data='', msg=project_not_exist_error)
            return jsonify(res.data)
        if model_id:
            exist_model = Model.query.filter_by(id=model_id, status=True).first()
            if not exist_model:
                res.update(code=-1, data='', msg=model_not_exist_error)
                return jsonify(res.data)
            if exist_model.project_id != project_id:
                res.update(code=-1, data='', msg=model_not_in_project)
                return jsonify(res.data)
        new_interface = Interface(
            Interface_name=interface_name,
            Interface_desc=interface_desc,
            interface_type=interface_type,
            method=method,
            path=path,
            project_id=project_id,
            model_id=model_id,
            c_uid=current_user.id
        )
        db.session.add(new_interface)
        try:
            db.session.commit()
            interface_info = {
                'interface_id': new_interface.id,
                'interface_name': interface_name,
            }
            res.update(code=1, data=interface_info, msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class EditInterface(MethodView):
    """编辑接口"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(edit_interface_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        interface_id = data.get('interface_id')
        interface_name = data.get('interface_name')
        interface_desc = data.get('interface_desc')
        interface_type = data.get('interface_type')
        method = data.get('method')
        path = data.get('path')
        exist_interface = Interface.query.filter_by(id=interface_id, status=True).first()
        if not exist_interface:
            res.update(code=-1, data='', msg=interface_not_exist_error)
            return jsonify(res.data)
        exist_interface.Interface_name = interface_name
        exist_interface.Interface_desc = interface_desc
        exist_interface.interface_type = interface_type
        exist_interface.method = method
        exist_interface.path = path
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class MoveInterface(MethodView):
    """移动接口"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(move_interface_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        project_id = data.get('project_id')
        model_id = data.get('model_id')
        interface_id = data.get('interface_id')
        exist_project = Project.query.filter_by(id=project_id, status=True).first()
        if not exist_project:
            res.update(code=-1, data='', msg=project_not_exist_error)
            return jsonify(res.data)
        if model_id:
            exist_model = Model.query.filter_by(id=model_id, status=True).first()
            if not exist_model:
                res.update(code=-1, data='', msg=model_not_exist_error)
                return jsonify(res.data)
            if exist_model.project_id != project_id:
                res.update(code=-1, data='', msg=model_not_in_project)
                return jsonify(res.data)
        exist_interface = Interface.query.filter_by(id=interface_id, status=True).first()
        if not exist_interface:
            res.update(code=-1, data='', msg=interface_not_exist_error)
            return jsonify(res.data)
        exist_interface.project_id = project_id
        exist_interface.model_id = model_id
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class DelInterface(MethodView):
    """删除接口"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(del_interface_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        interface_id = data.get('interface_id')
        exist_interface = Interface.query.filter_by(id=interface_id, status=True).first()
        if not exist_interface:
            res.update(code=-1, data='', msg=interface_not_exist_error)
            return jsonify(res.data)
        exist_interface.status = False
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class EditParam(MethodView):
    """编辑接口参数，先移除之前所有参数，再新增参数"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(edd_param_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        interface_id = data.get('interface_id')
        Parameter.query.filter_by(interface_id=interface_id).delete(synchronize_session=False)
        params = data.get('params')
        if len(params) > 0:
            for para in params:
                new_param = Parameter(
                    param_name=para.get('param_name'),
                    param_desc=para.get('param_desc'),
                    necessary=True if para.get('is_necessary') == 1 else False,
                    default=para.get('default'),
                    interface_id=interface_id,
                    c_uid=current_user.id
                )
                db.session.add(new_param)
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class EditHeader(MethodView):
    """编辑接口header"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(edit_header_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        interface_id = data.get('interface_id')
        header = data.get('header')
        if not is_json(header):
            res.update(code=-1, data=header, msg=param_not_json_error)
            return jsonify(res.data)
        exist_interface = Interface.query.filter_by(id=interface_id, status=True).first()
        if not exist_interface:
            res.update(code=-1, data='', msg=interface_not_exist_error)
            return jsonify(res.data)
        exist_interface.header = header
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class EditResponse(MethodView):
    """编辑接口response"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(edit_response_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        interface_id = data.get('interface_id')
        response = data.get('response')
        exist_interface = Interface.query.filter_by(id=interface_id, status=True).first()
        if not exist_interface:
            res.update(code=-1, data='', msg=interface_not_exist_error)
            return jsonify(res.data)
        exist_interface.response = response
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class ImportJsonData(MethodView):
    """批量导入json文件的接口信息"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(import_json_data_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        project_id = data.get('project_id')
        model_id = data.get('model_id')
        file_name = data.get('file_name')
        json_type = data.get('json_type')
        flag, data_list = ImportJson(file_name).get_data_list(json_type)
        if flag == -1:
            res.update(code=-1, data=data_list, msg=open_file_error)
            return jsonify(res.data)
        for data in data_list:
            new_interface = Interface(
                Interface_name=data['interface_name'],
                Interface_desc=data['interface_desc'],
                interface_type=data['interface_type'],
                method=data['method'],
                path=data['path'],
                header=data['header'],
                response=data['response'],
                project_id=project_id,
                model_id=model_id,
                c_uid=current_user.id
            )
            db.session.add(new_interface)
            db.session.flush()
            if len(data['params']) > 0:
                for para in data['params']:
                    new_param = Parameter(
                        param_name=para['param_name'],
                        param_desc=para['param_desc'],
                        necessary=para['necessary'],
                        default=para['default'],
                        interface_id=new_interface.id,
                        c_uid=current_user.id
                    )
                    db.session.add(new_param)
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)
