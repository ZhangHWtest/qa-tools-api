# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request, session
from flask.views import MethodView
from flask_login import login_required, login_user, logout_user, current_user
from apscheduler.triggers.cron import CronTrigger
from app import loginManager, cache, sched
from app.models import *
from .my_schema import *
from .data_statistics import case_data_statistics
from common.response import ResMsg
from common.response_message import *
from common.json_checker import format_checker

home = Blueprint('home', __name__)


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Index(MethodView):
    """首页"""
    @login_required
    @cache.cached(timeout=3600, key_prefix='view_%s')
    def get(self):
        res = ResMsg()
        day = 7
        case_stat = CaseStatistics.query.order_by(CaseStatistics.id.desc()).limit(day)
        if case_stat.count() == 0:
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        new_cs = case_stat.first()
        cs_date_list = []
        for cs in reversed(case_stat.all()):
            date_cs = {
                'open_date': cs.open_date,
                'today_run_case_num': cs.today_run_case_num,
                'today_suc_case_num': cs.today_suc_case_num,
                'today_fail_case_num': cs.today_fail_case_num,
            }
            cs_date_list.append(date_cs)
        data = {
            'interface_num': new_cs.interface_num,
            'case_num': new_cs.case_num,
            'run_case_num': new_cs.run_case_num,
            'success_case_num': new_cs.success_case_num,
            'failure_case_num': new_cs.failure_case_num,
            'exception_case_num': new_cs.exception_case_num,
            'cs_date_list': cs_date_list
        }
        res.update(code=1, data=data, msg=request_success)
        return jsonify(res.data)


class Register(MethodView):
    """注册"""
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(reg_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        username = data.get('username')
        password = data.get('password')
        set_password = data.get('set_password')
        user_email = data.get('email')
        if password != set_password:
            res.update(code=-1, data='', msg=password_not_same)
            return jsonify(res.data)
        user = User.query.filter_by(username=username).first()
        if user:
            res.update(code=-1, data='', msg=user_exist)
            return jsonify(res.data)
        email = User.query.filter_by(user_email=user_email).first()
        if email:
            res.update(code=-1, data='', msg=email_exist)
            return jsonify(res.data)
        new_user = User(username=username, user_email=user_email, role_id=1)
        new_user.set_password(password)
        db.session.add(new_user)
        user_info = {'user': username, 'user_role': 'User'}
        try:
            db.session.commit()
            # 需要邮箱发送的方法
            # msg = Message(u"你好", sender=email, recipients=email)
            # msg.body = u"欢迎你注册, 你的用户名：%s，你的密码是：%s" % (usernmae, pasword)
            # msg.html = '<a href="http://127.0.0.1:5000/login">去登录</a>'
            # Mail.send(msg)
            res.update(code=1, data=user_info, msg=registration_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=registration_failure)
            return jsonify(res.data)


class Login(MethodView):
    """登录"""
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(login_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            if user.status is False:
                res.update(code=-1, data='', msg=user_login_forbidden)
                return jsonify(res.data)
            if user.check_password(password):
                login_user(user)
                session['username'] = username
                session['role'] = user.role_id
                token = session['_id']
                data = {
                    'user': username,
                    'uid': user.id,
                    'user_role': user.role_id,
                    'token': token,
                }
                res.update(code=1, data=data, msg=login_success)
                return jsonify(res.data)
            else:
                res.update(code=-1, data='', msg=password_error)
                return jsonify(res.data)
        res.update(code=-1, data='', msg=user_not_exist)
        return jsonify(res.data)


class Logout(MethodView):
    """注销"""
    @login_required
    def get(self):
        res = ResMsg()
        session.clear()
        logout_user()
        res.update(code=1, data='', msg=logout_success)
        return jsonify(res.data)


class StartCaseStatistics(MethodView):
    """启动用例统计定时任务"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(statistics_task_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        password = data.get('password')
        if password != 'za-test':
            res.update(code=-1, data='', msg=password_error)
            return jsonify(res.data)
        run_time = '0 2 * * *'
        job_name = 'case_statistics_%s' % password
        try:
            if sched.get_job(job_name):
                mes = {'error': '缓存中已存在任务 %s 信息' % job_name}
                res.update(code=-1, data=mes, msg=task_start_error)
                return jsonify(res.data)
            # 标准crontab格式'5 2 * * *' 每天凌晨2点5分执行
            sched.add_job(case_data_statistics, CronTrigger.from_crontab(run_time), id=job_name, args=[],
                          jobstore='redis', replace_existing=True)
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            res.update(code=-1, data=str(e), msg=task_start_error)
            return jsonify(res.data)


class StopCaseStatistics(MethodView):
    """停止用例统计定时任务"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(statistics_task_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        password = data.get('password')
        if password != 'za-test':
            res.update(code=-1, data='', msg=password_error)
            return jsonify(res.data)
        job_name = 'case_statistics_%s' % password
        if sched.get_job(job_name):
            sched.remove_job(job_name)
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        else:
            mes = {'error': '缓存中不存在任务 %s 信息' % job_name}
            res.update(code=-1, data=mes, msg=task_stop_error)
            return jsonify(res.data)


class TestCaseStatistics(MethodView):
    """测试用例统计执行"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(test_statistics_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        password = data.get('password')
        day = data.get('day')
        save = data.get('save')
        if password != 'za-test':
            res.update(code=-1, data='', msg=password_error)
            return jsonify(res.data)
        save = True if save == 1 else False
        data = case_data_statistics(day, save)
        res.update(code=1, data=data, msg=request_success)
        return jsonify(res.data)
