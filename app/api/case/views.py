# -*- coding: utf-8 -*-

import time
import json
from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_login import login_required, current_user
from app import loginManager
from app.models import *
from .my_schema import *
# from .run_case import RunCase
from ..task.run_task import run_task
from common.response import ResMsg
from common.response_message import *
from common.return_list_page import list_page
from common.aksk_sign import make_aksk_sign
from common.requ_case import ApiRequest
from common.get_value import get_value_from_dict
from common.panduan import assert_contain
from common.json_checker import format_checker, is_json

case = Blueprint('case', __name__)


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class CaseList(MethodView):
    """
    用例列表
    model_id, project_id，interface_id都是非必填参数
    优先获取interface的接口，然后model下的接口，然后才是project下的接口
    都没有时，获取全部接口
    """
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(case_list_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        project_id = data.get('project_id')
        model_id = data.get('model_id')
        interface_id = data.get('interface_id')
        case_name = data.get('case_name') if data.get('case_name') is not None else ''
        page_num = data.get('page_num')
        page_size = data.get('page_size', 10)
        case_list = list()
        if interface_id:
            try:
                cases = TestCase.query.filter_by(interface_id=interface_id, status=True).filter(
                    TestCase.case_name.like('%' + case_name + '%')
                ).order_by(TestCase.id.desc()).all()
            except Exception as e:
                res.update(code=-1, data=str(e), msg=request_fail)
                return jsonify(res.data)
        elif model_id:
            try:
                interface_list = [x.id for x in Interface.query.filter_by(model_id=model_id, status=True)]
                cases = TestCase.query.filter(TestCase.status == True).filter(TestCase.interface_id.in_(interface_list))\
                    .filter(TestCase.case_name.like('%' + case_name + '%')).all()
                # cases = TestCase.query.filter_by(model_id=model_id, status=True)\
                #     .order_by(TestCase.id.desc()).all()
            except Exception as e:
                res.update(code=-1, data=str(e), msg=request_fail)
                return jsonify(res.data)
        elif project_id:
            try:
                interface_list = [x.id for x in Interface.query.filter_by(project_id=project_id, status=True)]
                cases = TestCase.query.filter(TestCase.status == True).filter(TestCase.interface_id.in_(interface_list))\
                    .filter(TestCase.case_name.like('%' + case_name + '%')).all()
                # cases = TestCase.query.filter_by(project_id=project_id, status=True)\
                #     .order_by(TestCase.id.desc()).all()
            except Exception as e:
                res.update(code=-1, data=str(e), msg=request_fail)
                return jsonify(res.data)
        else:
            try:
                cases = TestCase.query.filter_by(status=True).filter(
                    TestCase.case_name.like('%' + case_name + '%')
                ).order_by(TestCase.id.desc()).all()
            except Exception as e:
                res.update(code=-1, data=str(e), msg=request_fail)
                return jsonify(res.data)
        if cases:
            for c in cases:
                project_name = c.interfaces.projects.project_name if c.interfaces.project_id else ''
                model_name = c.interfaces.models.model_name if c.interfaces.model_id else ''
                interface_name = c.interfaces.Interface_name if c.interface_id else ''
                case_info = {
                    'case_id': c.id,
                    'case_name': c.case_name,
                    'case_type': c.case_type,
                    'method': c.method,
                    'url': c.environments.url,
                    'path': c.path,
                    'project_name': project_name,
                    'model_name': model_name,
                    'interface_name': interface_name,
                    'create_user': c.users.username,
                }
                case_list.append(case_info)
        data, total = list_page(case_list, page_size, page_num)
        res.update(code=1, data=data, msg=request_success)
        res.add_field(name='page_total_num', value=total)
        return jsonify(res.data)


class CaseInfo(MethodView):
    """用例信息"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(case_info_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        case_id = data.get('case_id')
        exist_case = TestCase.query.filter_by(id=case_id, status=True).first()
        if not exist_case:
            res.update(code=-1, data='', msg=case_not_exist_error)
            return jsonify(res.data)
        project_name = exist_case.interfaces.projects.project_name if exist_case.interfaces.project_id else ''
        model_name = exist_case.interfaces.models.model_name if exist_case.interfaces.model_id else ''
        rely_case = exist_case.rely_case.all()
        rely_list = list()
        if rely_case:
            has_rely = 1
            rely_param_list = json.loads(exist_case.rely_params)
            for x in range(len(rely_case)):
                rely_info = {
                    'rely_case_id': rely_case[x].id,
                    'rely_param': rely_param_list[x]
                }
                rely_list.append(rely_info)
        else:
            has_rely = 0
            rely_list = []
        exist_env = Environment.query.filter_by(id=exist_case.env_id, status=True).first()
        if not exist_env:
            env_info = {}
        else:
            env_info = {
                'env_id': exist_env.id,
                'env_name': exist_env.env_name,
                'url': exist_env.url,
                'use_db': 1 if exist_env.use_db else 0,
            }
        case_info = {
            'case_id': exist_case.id,
            'case_name': exist_case.case_name,
            'case_desc': exist_case.case_desc,
            'case_type': exist_case.case_type,
            'method': exist_case.method,
            'path': exist_case.path,
            'params': exist_case.params,
            'header': exist_case.header,
            'has_sign': exist_case.has_sign,
            'ak': exist_case.ak,
            'sk': exist_case.sk,
            'res_assert': exist_case.res_assert,
            'has_rely': has_rely,
            'rely_info': json.dumps(rely_list, ensure_ascii=False),
            'has_output': exist_case.has_output,
            'output_para': exist_case.output_para,
            'has_input': exist_case.has_input,
            'input_para': exist_case.input_para,
            'input_header': exist_case.input_header,
            'is_debug': 1 if exist_case.is_debug is True else 0,
            'is_pass': 1 if exist_case.is_pass is True else 0,
            'save_result': 1 if exist_case.save_result is True else 0,
            'use_db': 1 if exist_case.use_db is True else 0,
            'sql': exist_case.sql if exist_case.sql else '',
            'field_value': exist_case.field_value if exist_case.field_value else '',
            'project_name': project_name,
            'model_name': model_name,
            'interface_name': exist_case.interfaces.Interface_name,
            'env_info': env_info,
            'create_user': exist_case.users.username,
        }
        res.update(code=1, data=case_info, msg=request_success)
        return jsonify(res.data)


class AddCase(MethodView):
    """新增用例"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(add_case_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        interface_id = data.get('interface_id')
        env_id = data.get('env_id')
        case_name = data.get('case_name')
        case_desc = data.get('case_desc')
        case_type = data.get('case_type')
        method = data.get('method')
        path = data.get('path')
        params = data.get('params')
        header = data.get('header')
        has_sign = data.get('has_sign')
        ak = data.get('ak')
        sk = data.get('sk')
        res_assert = data.get('res_assert')
        has_rely = data.get('has_rely')
        rely_info = data.get('rely_info')
        has_output = data.get('has_output')
        output_para = data.get('output_para')
        has_input = data.get('has_input')
        input_para = data.get('input_para')
        input_header = data.get('input_header')
        save_result = data.get('save_result')
        use_db = data.get('use_db')
        sql = data.get('sql')
        field_value = data.get('field_value')
        exist_interface = Interface.query.filter_by(id=interface_id, status=True).first()
        if not exist_interface:
            res.update(code=-1, data='', msg=interface_not_exist_error)
            return jsonify(res.data)
        exist_env = Environment.query.filter_by(id=env_id, status=True).first()
        if not exist_env:
            res.update(code=-1, data='', msg=env_not_exist_error)
            return jsonify(res.data)
        if not is_json(params):
            res.update(code=-1, data=params, msg=param_not_json_error)
            return jsonify(res.data)
        if not is_json(header):
            res.update(code=-1, data=header, msg=param_not_json_error)
            return jsonify(res.data)
        if not is_json(res_assert):
            res.update(code=-1, data=res_assert, msg=param_not_json_error)
            return jsonify(res.data)
        rely_case_list = list()
        rely_params = list()
        if has_rely:
            if not rely_info:
                res.update(code=-1, data='', msg=param_empty_error)
                return jsonify(res.data)
            if not is_json(rely_info):
                res.update(code=-1, data=rely_info, msg=param_not_json_error)
                return jsonify(res.data)
            rely_info = json.loads(rely_info)
            for rc in rely_info:
                rely_case_id = rc['rely_case_id']
                rely_case = TestCase.query.filter_by(id=rely_case_id, status=True).first()
                if not rely_case:
                    res.update(code=-1, data='', msg=rely_case_not_exist_error)
                    return jsonify(res.data)
                if rely_case.rely_case.all():
                    res.update(code=-1, data='', msg=rely_case_has_rely_error)
                    return jsonify(res.data)
                if rely_case in rely_case_list:
                    res.update(code=-1, data='', msg=rely_case_same_error)
                    return jsonify(res.data)
                rely_case_list.append(rely_case)
                rely_params.append(rc['rely_param'])    # 每个依赖用例只能输出一个依赖参数
        if has_output == 1:
            if not output_para:
                res.update(code=-1, data='', msg=output_param_empty_error)
                return jsonify(res.data)
        else:
            output_para = ''
        if has_input == 1:
            if not input_para and not input_header:
                res.update(code=-1, data='', msg=input_param_empty_error)
                return jsonify(res.data)
        else:
            input_para = ''
            input_header = ''
        # save_result = True if save_result == 1 else False
        # 必须保存用例执行结果
        save_result = True
        use_db = True if use_db == 1 else False
        if use_db:
            if sql and field_value:
                pass
            else:
                res.update(code=-1, data='', msg=db_info_empty_error)
                return jsonify(res.data)
        else:
            sql = field_value = ''
        new_case = TestCase(
            case_name=case_name,
            case_desc=case_desc,
            case_type=case_type,
            method=method,
            path=path,
            params=params,
            header=header,
            has_sign=has_sign,
            ak=ak,
            sk=sk,
            res_assert=res_assert,
            has_output=has_output,
            output_para=output_para,
            has_input=has_input,
            input_para=input_para,
            input_header=input_header,
            save_result=save_result,
            use_db=use_db,
            sql=sql,
            field_value=field_value,
            project_id=exist_interface.project_id,
            model_id=exist_interface.model_id,
            interface_id=interface_id,
            env_id=env_id,
            c_uid=current_user.id
        )
        db.session.add(new_case)
        db.session.flush()
        if has_rely:
            for rely_case in rely_case_list:
                new_case.rely_case.append(rely_case)
            new_case.rely_params = json.dumps(rely_params, ensure_ascii=False)
        try:
            db.session.commit()
            case_info = {
                'case_id': new_case.id,
                'case_name': case_name,
            }
            res.update(code=1, data=case_info, msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class EditCase(MethodView):
    """编辑用例"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(edit_case_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        case_id = data.get('case_id')
        env_id = data.get('env_id')
        case_name = data.get('case_name')
        case_desc = data.get('case_desc')
        case_type = data.get('case_type')
        method = data.get('method')
        path = data.get('path')
        params = data.get('params')
        header = data.get('header')
        has_sign = data.get('has_sign')
        ak = data.get('ak')
        sk = data.get('sk')
        res_assert = data.get('res_assert')
        has_rely = data.get('has_rely')
        rely_info = data.get('rely_info')
        has_output = data.get('has_output')
        output_para = data.get('output_para')
        has_input = data.get('has_input')
        input_para = data.get('input_para')
        input_header = data.get('input_header')
        save_result = data.get('save_result')
        use_db = data.get('use_db')
        sql = data.get('sql')
        field_value = data.get('field_value')
        exist_env = Environment.query.filter_by(id=env_id, status=True).first()
        if not exist_env:
            res.update(code=-1, data='', msg=env_not_exist_error)
            return jsonify(res.data)
        if not is_json(params):
            res.update(code=-1, data=params, msg=param_not_json_error)
            return jsonify(res.data)
        if not is_json(header):
            res.update(code=-1, data=header, msg=param_not_json_error)
            return jsonify(res.data)
        if not is_json(res_assert):
            res.update(code=-1, data=res_assert, msg=param_not_json_error)
            return jsonify(res.data)
        rely_case_list = list()
        rely_params = list()
        if has_rely:
            if not rely_info:
                res.update(code=-1, data='', msg=param_empty_error)
                return jsonify(res.data)
            if not is_json(rely_info):
                res.update(code=-1, data=rely_info, msg=param_not_json_error)
                return jsonify(res.data)
            rely_info = json.loads(rely_info)
            for rc in rely_info:
                rely_case_id = rc['rely_case_id']
                if rely_case_id == case_id:
                    res.update(code=-1, data='', msg=rely_case_self_error)
                    return jsonify(res.data)
                rely_case = TestCase.query.filter_by(id=rely_case_id, status=True).first()
                if not rely_case:
                    res.update(code=-1, data='', msg=rely_case_not_exist_error)
                    return jsonify(res.data)
                if rely_case.rely_case.all():
                    res.update(code=-1, data='', msg=rely_case_has_rely_error)
                    return jsonify(res.data)
                if rely_case in rely_case_list:
                    res.update(code=-1, data='', msg=rely_case_same_error)
                    return jsonify(res.data)
                rely_case_list.append(rely_case)
                rely_params.append(rc['rely_param'])
        if has_output == 1:
            if not output_para:
                res.update(code=-1, data='', msg=output_param_empty_error)
                return jsonify(res.data)
        else:
            output_para = ''
        if has_input == 1:
            if not input_para and not input_header:
                res.update(code=-1, data='', msg=input_param_empty_error)
                return jsonify(res.data)
        else:
            input_para = ''
            input_header = ''
        # save_result = True if save_result == 1 else False
        use_db = True if use_db == 1 else False
        if use_db:
            if sql and field_value:
                pass
            else:
                res.update(code=-1, data='', msg=db_info_empty_error)
                return jsonify(res.data)
        else:
            sql = field_value = ''
        exist_case = TestCase.query.filter_by(id=case_id, status=True).first()
        if not exist_case:
            res.update(code=-1, data='', msg=case_not_exist_error)
            return jsonify(res.data)
        exist_case.case_name = case_name
        exist_case.case_desc = case_desc
        exist_case.case_type = case_type
        exist_case.method = method
        exist_case.path = path
        exist_case.params = params
        exist_case.header = header
        exist_case.has_sign = has_sign
        exist_case.ak = ak
        exist_case.sk = sk
        exist_case.res_assert = res_assert
        exist_case.has_output = has_output
        exist_case.output_para = output_para
        exist_case.has_input = has_input
        exist_case.input_para = input_para
        exist_case.input_header = input_header
        # exist_case.save_result = save_result
        exist_case.use_db = use_db
        exist_case.sql = sql
        exist_case.field_value = field_value
        exist_case.env_id = env_id
        for exist_rc in exist_case.rely_case.all():
            exist_case.rely_case.remove(exist_rc)
        if has_rely:
            for rely_case in rely_case_list:
                exist_case.rely_case.append(rely_case)
            exist_case.rely_params = json.dumps(rely_params, ensure_ascii=False)
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class DuplicateCase(MethodView):
    """复制用例副本"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(duplicate_case_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        case_id = data.get('case_id')
        exist_case = TestCase.query.filter_by(id=case_id, status=True).first()
        if not exist_case:
            res.update(code=-1, data='', msg=case_not_exist_error)
            return jsonify(res.data)
        new_case = TestCase(
            case_name=exist_case.case_name,
            case_desc=exist_case.case_desc,
            case_type=exist_case.case_type,
            method=exist_case.method,
            path=exist_case.path,
            params=exist_case.params,
            header=exist_case.header,
            has_sign=exist_case.has_sign,
            ak=exist_case.ak,
            sk=exist_case.sk,
            res_assert=exist_case.res_assert,
            rely_params=exist_case.rely_params,
            has_output=exist_case.has_output,
            output_para=exist_case.output_para,
            has_input=exist_case.has_input,
            input_para=exist_case.input_para,
            input_header=exist_case.input_header,
            save_result=exist_case.save_result,
            use_db=exist_case.use_db,
            sql=exist_case.sql,
            field_value=exist_case.field_value,
            project_id=exist_case.project_id,
            model_id=exist_case.model_id,
            interface_id=exist_case.interface_id,
            env_id=exist_case.env_id,
            c_uid=current_user.id
        )
        db.session.add(new_case)
        db.session.flush()
        for exist_rc in exist_case.rely_case.all():
            new_case.rely_case.append(exist_rc)
        try:
            db.session.commit()
            case_info = {
                'case_id': new_case.id,
                'case_name': new_case.case_name,
            }
            res.update(code=1, data=case_info, msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class DelCase(MethodView):
    """删除用例"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(del_case_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        case_id = data.get('case_id')
        exist_case = TestCase.query.filter_by(id=case_id, status=True).first()
        if not exist_case:
            res.update(code=-1, data='', msg=case_not_exist_error)
            return jsonify(res.data)
        exist_case.status = False
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class RunSingleCase(MethodView):
    """执行单个用例"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(run_single_case_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        case_id = data.get('case_id')
        exist_case = TestCase.query.filter_by(id=case_id, status=True).first()
        if not exist_case:
            res.update(code=-1, data='', msg=case_not_exist_error)
            return jsonify(res.data)
        exist_env = Environment.query.filter_by(id=exist_case.env_id, status=True).first()
        if not exist_env:
            res.update(code=-1, data='', msg=env_not_exist_error)
            return jsonify(res.data)
        method = exist_case.method
        path = exist_env.url + exist_case.path
        params = json.loads(exist_case.params)
        header = json.loads(exist_case.header)
        res_assert = json.loads(exist_case.res_assert)
        rely_cases = exist_case.rely_case.all()
        if rely_cases:  # 执行依赖用例，加入依赖参数的key,value
            rely_param_list = json.loads(exist_case.rely_params)
            for x in range(len(rely_cases)):
                rely_case = TestCase.query.filter_by(id=rely_cases[x].id, status=True).first()
                if not rely_case:
                    res.update(code=-1, data='', msg=rely_case_not_exist_error)
                    return jsonify(res.data)
                try:
                    api = ApiRequest(
                        url=rely_case.environments.url + rely_case.path,
                        method=rely_case.method,
                        params=json.loads(rely_case.params) if rely_case.params else '',
                        headers=json.loads(rely_case.header) if rely_case.header else ''
                    )
                    r, s = api.test_api()
                except Exception as e:
                    res.update(code=-1, data=str(e), msg=request_fail)
                    return jsonify(res.data)
                rely_param = rely_param_list[x]
                rely_param_value = get_value_from_dict(r, rely_param)
                if rely_param_value is None:
                    res.update(code=-1, data='', msg=rely_case_none_error)
                    return jsonify(res.data)
                params.update({rely_param: rely_param_value})
        ip_info, ih_info, input_info, op_info = ['', '', '', '']
        has_input = exist_case.has_input
        if has_input == 1:
            input_para = exist_case.input_para
            input_header = exist_case.input_header
            if input_para:
                ip_info = dict()
                ip_list = input_para.split(',')
                for ip in ip_list:
                    ip_info[ip] = '没有参数入参信息'
            if input_header:
                ih_info = dict()
                ih_list = input_header.split(',')
                for ih in ih_list:
                    ih_info[ih] = '没有header入参信息'
            input_info = {
                'input_para': ip_info,
                'input_header': ih_info
            }
        has_sign = exist_case.has_sign
        aksk_header = dict()
        if has_sign == 1:
            ak = exist_case.ak
            sk = exist_case.sk
            aksk_header = make_aksk_sign(ak, sk, params)
            header.update(aksk_header)
        try:
            api = ApiRequest(url=path, method=method, params=params, headers=header)
            result, duration = api.test_api()
        except Exception as e:
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)
        # if duration == -1:
        #     res.update(code=-1, data=result, msg=request_fail)
        #     return jsonify(res.data)
        has_output = exist_case.has_output
        if has_output == 1:
            output_para = exist_case.output_para
            op_info = dict()
            op_list = output_para.split(',')
            for op in op_list:
                opv = get_value_from_dict(result, op)
                op_info[op] = opv
        diff_res = assert_contain(res_assert, result)
        is_pass = 0 if diff_res else 1
        exist_case.is_debug = True
        exist_case.is_pass = is_pass
        if exist_case.save_result:
            new_case_res = CaseResult(
                case_type=exist_case.case_type,
                method=method,
                path=path,
                params=json.dumps(params, ensure_ascii=False),
                input_para=json.dumps(ip_info, ensure_ascii=False),
                header=json.dumps(header, ensure_ascii=False),
                input_header=json.dumps(ih_info, ensure_ascii=False),
                aksk_header=json.dumps(aksk_header, ensure_ascii=False),
                res_assert=exist_case.res_assert,
                case_result=is_pass,
                response=json.dumps(result, ensure_ascii=False),
                output_para=json.dumps(op_info, ensure_ascii=False),
                diff_res=json.dumps(diff_res, ensure_ascii=False),
                duration=duration,
                case_id=case_id,
                environment=exist_case.env_id
            )
            db.session.add(new_case_res)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)
        if has_input == 1:
            res.update(code=-1, data=input_info, msg=need_input_error)
            return jsonify(res.data)
        if is_pass:
            res.update(code=1, data='', msg=case_run_success)
            return jsonify(res.data)
        else:
            res.update(code=-1, data=diff_res, msg=case_run_fail)
            return jsonify(res.data)


class RunMultipleCase(MethodView):
    """创建任务，执行单个或多个用例，最多10个用例"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(run_multiple_case_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        project_id = data.get('project_id')
        case_list = data.get('case_list')
        day = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        task_name = "执行用例任务_%s" % day
        # project = Project.query.filter_by(id=project_id, status=True).first()
        # if not project:
        #     res.update(code=-1, data='', msg=project_not_exist_error)
        #     return jsonify(res.data)
        new_task = Task(
            task_name=task_name,
            task_type=0,
            run_time='',
            run_status=1,
            c_uid=current_user.id,
            s_uid=current_user.id,
            project_id=project_id,
        )
        db.session.add(new_task)
        db.session.flush()
        add_case_list, err_case_list, debug_case_list = [[], [], []]
        for case_id in case_list:
            exist_case = TestCase.query.filter_by(id=case_id, status=True).first()
            if exist_case:
                if not exist_case.is_debug:
                    debug_case_list.append(case_id)
                    continue
                new_task.interface.append(exist_case)
                add_case_list.append(case_id)
            else:
                err_case_list.append(case_id)
        case_info = {
            'add_case': add_case_list,
            'err_case': err_case_list,
            'debug_case': debug_case_list,
        }
        if len(add_case_list) == 0:
            db.session.rollback()
            res.update(code=-1, data=case_info, msg=task_add_case_error)
            return jsonify(res.data)
        try:
            db.session.commit()
            run_task(new_task.id, current_user.id, day)
            res.update(code=1, data=case_info, msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class CaseResList(MethodView):
    """用例测试结果列表"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(case_res_list_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        case_id = data.get('case_id')
        page_num = data.get('page_num')
        page_size = data.get('page_size', 10)
        case_res_list = list()
        exist_case = TestCase.query.filter_by(id=case_id, status=True).first()
        if not exist_case:
            res.update(code=-1, data='', msg=case_not_exist_error)
            return jsonify(res.data)
        try:
            case_results = CaseResult.query.filter_by(case_id=case_id).order_by(CaseResult.id.desc()).all()
        except Exception as e:
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)
        if case_results:
            for cr in case_results:
                case_info = {
                    'case_result_id': cr.id,
                    'case_type': cr.case_type,
                    'method': cr.method,
                    'path': cr.path,
                    'case_result': cr.case_result,
                    'start_time': datetime.datetime.strftime(cr.start_time, "%Y-%m-%d %H:%M:%S"),
                }
                case_res_list.append(case_info)
        data, total = list_page(case_res_list, page_size, page_num)
        res.update(code=1, data=data, msg=request_success)
        res.add_field(name='page_total_num', value=total)
        return jsonify(res.data)


class CaseResInfo(MethodView):
    """用例测试结果详情"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(case_res_info_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        case_result_id = data.get('case_result_id')
        case_result = CaseResult.query.filter_by(id=case_result_id).first()
        if not case_result:
            res.update(code=-1, data='', msg=case_res_not_exist_error)
            return jsonify(res.data)
        exist_case = TestCase.query.filter_by(id=case_result.case_id, status=True).first()
        if not exist_case:
            res.update(code=-1, data='', msg=case_not_exist_error)
            return jsonify(res.data)
        case_info = {
            'case_result_id': case_result.id,
            'case_name': exist_case.case_name,
            'case_type': case_result.case_type,
            'method': case_result.method,
            'path': case_result.path,
            'params': case_result.params,
            'input_para': case_result.input_para,
            'header': case_result.header,
            'input_header': case_result.input_header,
            'aksk_header': case_result.aksk_header,
            'res_assert': case_result.res_assert,
            'case_result': case_result.case_result,
            'response': case_result.response,
            'output_para': case_result.output_para,
            'diff_res': case_result.diff_res,
            'start_time': datetime.datetime.strftime(case_result.start_time, "%Y-%m-%d %H:%M:%S"),
            'duration': case_result.duration,
            'task_name': case_result.tasks.task_name if case_result.task_id else '',
        }
        res.update(code=1, data=case_info, msg=request_success)
        return jsonify(res.data)
