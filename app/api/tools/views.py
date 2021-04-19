# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_login import login_required
from app import loginManager
from app.models import *
from .my_schema import *
from .live_lesson_info import *
from .user_course_info import *
from common.response import ResMsg
from common.response_message import *
from common.pager import Pager
from common.json_checker import format_checker

tools = Blueprint('tools', __name__)


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LiveLessonToday(MethodView):
    """获取今日直播课信息接口"""
    @login_required
    # @cache.cached(timeout=1800, key_prefix='view_%s')
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(LiveLessonToday_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        page_size = data.get('pageSize')
        page_num = data.get('pageNum')
        data = get_live_lesson_today()
        if data is False:
            res.update(code=-1, data='', msg=lld_locked)
            return jsonify(res.data)
        pager = Pager(data, page_size)
        data = pager.page_data(page_num)
        res.update(code=1, data=data, msg=request_success)
        res.add_field(name='page_size', value=pager.page_size)
        res.add_field(name='page_num', value=page_num)
        res.add_field(name='page_total', value=pager.page_total_num)
        res.add_field(name='data_total', value=pager.data_count)
        return jsonify(res.data)


class LiveLessonYesterday(MethodView):
    """获取昨日直播课信息接口"""
    @login_required
    # @cache.cached(timeout=1800, key_prefix='view_%s')
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(LiveLessonToday_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        page_size = data.get('pageSize')
        page_num = data.get('pageNum')
        data = get_live_lesson_yesterday()
        if data is False:
            res.update(code=-1, data='', msg=lld_locked)
            return jsonify(res.data)
        pager = Pager(data, page_size)
        data = pager.page_data(page_num)
        res.update(code=1, data=data, msg=request_success)
        res.add_field(name='page_size', value=pager.page_size)
        res.add_field(name='page_num', value=page_num)
        res.add_field(name='page_total', value=pager.page_total_num)
        res.add_field(name='data_total', value=pager.data_count)
        return jsonify(res.data)


class CourseInfoByMobile(MethodView):
    """根据学员mobile获取学员的课程信息"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(CourseInfoByMobile_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        mobile = data.get('mobile')
        page_size = data.get('pageSize')
        page_num = data.get('pageNum')
        data = get_course_info_by_mobile(mobile)
        pager = Pager(data, page_size)
        data = pager.page_data(page_num)
        res.update(code=1, data=data, msg=request_success)
        res.add_field(name='page_size', value=pager.page_size)
        res.add_field(name='page_num', value=page_num)
        res.add_field(name='page_total', value=pager.page_total_num)
        res.add_field(name='data_total', value=pager.data_count)
        return jsonify(res.data)


class AuthRecordByMobile(MethodView):
    """根据学员mobile获取学员的授权信息"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(AuthRecordByMobile_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        mobile = data.get('mobile')
        page_size = data.get('pageSize')
        page_num = data.get('pageNum')
        data = get_course_auth_record_by_mobile(mobile)
        pager = Pager(data, page_size)
        data = pager.page_data(page_num)
        res.update(code=1, data=data, msg=request_success)
        res.add_field(name='page_size', value=pager.page_size)
        res.add_field(name='page_num', value=page_num)
        res.add_field(name='page_total', value=pager.page_total_num)
        res.add_field(name='data_total', value=pager.data_count)
        return jsonify(res.data)


class UserInfoByXid(MethodView):
    """根据订单xid获取学员信息"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(UserInfoByXid_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        xid = data.get('xid')
        data = get_user_info_by_xid(xid)
        pager = Pager(data)
        data = pager.page_data()
        res.update(code=1, data=data, msg=request_success)
        res.add_field(name='data_total', value=pager.data_count)
        return jsonify(res.data)


class CourseInfoByLiveId(MethodView):
    """根据订单xid获取学员信息"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(CourseInfoByLiveId_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        live_id = data.get('live_id')
        data = get_teacher_info_by_live_id(live_id)
        res.update(code=1, data=data, msg=request_success)
        return jsonify(res.data)
