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

equipment = Blueprint('equipment', __name__)


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class ManufacturerList(MethodView):
    """厂商列表"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(mf_list_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        page_num = data.get('page_num')
        page_size = data.get('page_size', 10)
        mf_list = list()
        try:
            mfs = Manufacturer.query.filter_by(status=1).all()
        except Exception as e:
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)
        if mfs:
            for mf in mfs:
                mf_info = {
                    'mf_id': mf.id,
                    'mf_name': mf.name,
                }
                mf_list.append(mf_info)
        data, total = list_page(mf_list, page_size, page_num)
        res.update(code=1, data=data, msg=request_success)
        res.add_field(name='page_total_num', value=total)
        return jsonify(res.data)


class AddManufacturer(MethodView):
    """新增厂商"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(add_mf_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        mf_name = data.get('mf_name')
        exist_mf = Manufacturer.query.filter_by(name=mf_name, status=1).first()
        if exist_mf:
            res.update(code=-1, data='', msg=mf_name_exist)
            return jsonify(res.data)
        new_eq = Manufacturer(name=mf_name)
        db.session.add(new_eq)
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class DelManufacturer(MethodView):
    """删除厂商"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(del_mf_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        mf_id = data.get('mf_id')
        exist_mf = Manufacturer.query.filter_by(id=mf_id, status=1).first()
        if not exist_mf:
            res.update(code=-1, data='', msg=mf_not_exist_error)
            return jsonify(res.data)
        exist_eq = Equipment.query.filter_by(mf_id=mf_id, status=1).first()
        if exist_eq:
            print(exist_eq)
            res.update(code=-1, data='', msg=mf_is_related_error)
            return jsonify(res.data)
        exist_mf.status = 0
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class EquipmentList(MethodView):
    """设备列表"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(eq_list_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        page_num = data.get('page_num')
        page_size = data.get('page_size', 10)
        eq_list = list()
        try:
            equip = Equipment.query.filter_by(status=1).order_by(Equipment.id.desc()).all()
        except Exception as e:
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)
        if equip:
            for eq in equip:
                eq_info = {
                    'eq_id': eq.id,
                    'eq_code': eq.eq_code,
                    'eq_name': eq.eq_name,
                    'eq_type': eq.eq_type,
                    'eq_sys': eq.eq_sys,
                    'eq_sys_ver': eq.eq_sys_ver,
                    'eq_owner': eq.eq_owner,
                    'borrower': eq.borrower,
                    'have_sim': eq.have_sim,
                    'eq_status': eq.eq_status,
                    'mf_name': eq.manufacturers.name,
                }
                eq_list.append(eq_info)
        data, total = list_page(eq_list, page_size, page_num)
        res.update(code=1, data=data, msg=request_success)
        res.add_field(name='page_total_num', value=total)
        return jsonify(res.data)


class EquipmentInfo(MethodView):
    """设备信息"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(eq_info_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        eq_id = data.get('eq_id')
        exist_eq = Equipment.query.filter_by(id=eq_id, status=1).first()
        if not exist_eq:
            res.update(code=-1, data='', msg=eq_not_exist_error)
            return jsonify(res.data)
        eq_info = {
            'eq_id': exist_eq.id,
            'eq_code': exist_eq.eq_code,
            'eq_name': exist_eq.eq_name,
            'eq_desc': exist_eq.eq_desc,
            'eq_type': exist_eq.eq_type,
            'eq_sys': exist_eq.eq_sys,
            'eq_sys_ver': exist_eq.eq_sys_ver,
            'eq_owner': exist_eq.eq_owner,
            'borrower': exist_eq.borrower,
            'have_sim': exist_eq.have_sim,
            'eq_status': exist_eq.eq_status,
            'mf_id': exist_eq.mf_id,
        }
        res.update(code=1, data=eq_info, msg=request_success)
        return jsonify(res.data)


class AddEquipment(MethodView):
    """新增设备"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(add_eq_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        eq_code = data.get('eq_code')
        eq_name = data.get('eq_name')
        eq_desc = data.get('eq_desc')
        eq_type = data.get('eq_type')
        eq_sys = data.get('eq_sys')
        eq_sys_ver = data.get('eq_sys_ver')
        eq_owner = data.get('eq_owner')
        have_sim = data.get('have_sim')
        mf_id = data.get('mf_id')
        exist_eq = Equipment.query.filter_by(eq_code=eq_code, status=1).first()
        if exist_eq:
            res.update(code=-1, data='', msg=eq_code_exist_error)
            return jsonify(res.data)
        new_eq = Equipment(
            eq_code=eq_code,
            eq_name=eq_name,
            eq_desc=eq_desc,
            eq_type=eq_type,
            eq_sys=eq_sys,
            eq_sys_ver=eq_sys_ver,
            eq_owner=eq_owner,
            have_sim=have_sim,
            mf_id=mf_id
        )
        db.session.add(new_eq)
        try:
            db.session.commit()
            eq_info = {
                'eq_code': eq_code,
                'eq_name': eq_name,
                'eq_desc': eq_desc,
                'eq_type': eq_type,
                'eq_sys': eq_sys,
                'eq_sys_ver': eq_sys_ver,
                'eq_owner': eq_owner,
                'borrower': '',
                'have_sim': have_sim,
                'mf_id': mf_id,
                'eq_id': new_eq.id
            }
            add_eq_log(eq_info, 1)
            res.update(code=1, data=eq_info, msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class EditEquipment(MethodView):
    """编辑设备"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(edit_eq_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        eq_id = data.get('eq_id')
        eq_code = data.get('eq_code')
        eq_name = data.get('eq_name')
        eq_desc = data.get('eq_desc')
        eq_type = data.get('eq_type')
        eq_sys = data.get('eq_sys')
        eq_sys_ver = data.get('eq_sys_ver')
        eq_owner = data.get('eq_owner')
        borrower = data.get('borrower')
        have_sim = data.get('have_sim')
        mf_id = data.get('mf_id')
        exist_eq = Equipment.query.filter_by(id=eq_id, status=1).first()
        if not exist_eq:
            res.update(code=-1, data='', msg=eq_not_exist_error)
            return jsonify(res.data)
        other_eq = Equipment.query.filter_by(eq_code=eq_code, status=1).first()
        if other_eq and other_eq != exist_eq:
            res.update(code=-1, data='', msg=eq_code_exist_error)
            return jsonify(res.data)
        exist_eq.eq_code = eq_code
        exist_eq.eq_name = eq_name
        exist_eq.eq_desc = eq_desc
        exist_eq.eq_type = eq_type
        exist_eq.eq_sys = eq_sys
        exist_eq.eq_sys_ver = eq_sys_ver
        exist_eq.eq_owner = eq_owner
        exist_eq.borrower = borrower
        exist_eq.have_sim = have_sim
        exist_eq.mf_id = mf_id
        try:
            db.session.commit()
            eq_info = {
                'eq_code': eq_code,
                'eq_name': eq_name,
                'eq_desc': eq_desc,
                'eq_type': eq_type,
                'eq_sys': eq_sys,
                'eq_sys_ver': eq_sys_ver,
                'eq_owner': eq_owner,
                'borrower': borrower,
                'have_sim': have_sim,
                'mf_id': mf_id,
                'eq_id': eq_id
            }
            add_eq_log(eq_info, 2)
            res.update(code=1, data=eq_info, msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class SwitchEquipment(MethodView):
    """切换设备停用/可外借/已外借状态"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(switch_eq_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        eq_id = data.get('eq_id')
        borrower = data.get('borrower')
        eq_status = data.get('eq_status')
        exist_eq = Equipment.query.filter_by(id=eq_id, status=1).first()
        if not exist_eq:
            res.update(code=-1, data='', msg=eq_not_exist_error)
            return jsonify(res.data)
        if eq_status == 0:
            log_status = 0
            borrower = ''
        elif eq_status == 1 and borrower == '':
            log_status = 3
        elif eq_status == 2 and borrower != '':
            log_status = 4
        else:
            res.update(code=-1, data={'eq_status': eq_status, 'borrower': borrower}, msg=param_error)
            return jsonify(res.data)
        exist_eq.borrower = borrower
        exist_eq.eq_status = eq_status
        try:
            db.session.commit()
            eq_info = {
                'eq_code': exist_eq.eq_code,
                'eq_name': exist_eq.eq_name,
                'eq_desc': exist_eq.eq_desc,
                'eq_type': exist_eq.eq_type,
                'eq_sys': exist_eq.eq_sys,
                'eq_sys_ver': exist_eq.eq_sys_ver,
                'eq_owner': exist_eq.eq_owner,
                'borrower': exist_eq.borrower,
                'have_sim': exist_eq.have_sim,
                'mf_id': exist_eq.mf_id,
                'eq_id': exist_eq.id
            }
            add_eq_log(eq_info, log_status)
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class DelEquipment(MethodView):
    """删除设备"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(del_eq_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        eq_id = data.get('eq_id')
        exist_eq = Equipment.query.filter_by(id=eq_id, status=1).first()
        if not exist_eq:
            res.update(code=-1, data='', msg=eq_not_exist_error)
            return jsonify(res.data)
        exist_eq.status = 0
        try:
            db.session.commit()
            eq_info = {
                'eq_code': exist_eq.eq_code,
                'eq_name': exist_eq.eq_name,
                'eq_desc': exist_eq.eq_desc,
                'eq_type': exist_eq.eq_type,
                'eq_sys': exist_eq.eq_sys,
                'eq_sys_ver': exist_eq.eq_sys_ver,
                'eq_owner': exist_eq.eq_owner,
                'borrower': exist_eq.borrower,
                'have_sim': exist_eq.have_sim,
                'mf_id': exist_eq.mf_id,
                'eq_id': exist_eq.id
            }
            add_eq_log(eq_info, 5)
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class EquipmentLogList(MethodView):
    """设备日志列表"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(eq_log_list_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        eq_id = data.get('eq_id')
        page_num = data.get('page_num')
        page_size = data.get('page_size', 10)
        eq_log_list = list()
        exist_eq = Equipment.query.filter_by(id=eq_id, status=1).first()
        if not exist_eq:
            res.update(code=-1, data='', msg=eq_not_exist_error)
            return jsonify(res.data)
        try:
            equip_log = EquipmentLog.query.filter_by(eq_id=eq_id).order_by(EquipmentLog.id.desc()).all()
        except Exception as e:
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)
        if equip_log:
            for el in equip_log:
                eq_log = {
                    'eq_log_id': el.id,
                    'eq_code': el.eq_code,
                    'eq_name': el.eq_name,
                    'eq_desc': el.eq_desc,
                    'eq_type': el.eq_type,
                    'eq_sys': el.eq_sys,
                    'eq_sys_ver': el.eq_sys_ver,
                    'eq_owner': el.eq_owner,
                    'borrower': el.borrower,
                    'have_sim': el.have_sim,
                    'eq_log_status': el.status,
                    'mf_name': el.manufacturers.name,
                    'c_user': el.users.username,
                }
                eq_log_list.append(eq_log)
        data, total = list_page(eq_log_list, page_size, page_num)
        res.update(code=1, data=data, msg=request_success)
        res.add_field(name='page_total_num', value=total)
        return jsonify(res.data)


def add_eq_log(eq_info, status):
    new_eq_log = EquipmentLog(
        eq_code=eq_info['eq_code'],
        eq_name=eq_info['eq_name'],
        eq_desc=eq_info['eq_desc'],
        eq_type=eq_info['eq_type'],
        eq_sys=eq_info['eq_sys'],
        eq_sys_ver=eq_info['eq_sys_ver'],
        eq_owner=eq_info['eq_owner'],
        borrower=eq_info['borrower'],
        have_sim=eq_info['have_sim'],
        status=status,
        mf_id=eq_info['mf_id'],
        eq_id=eq_info['eq_id'],
        c_uid=current_user.id
    )
    db.session.add(new_eq_log)
    try:
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False
