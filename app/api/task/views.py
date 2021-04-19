# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_login import login_required, current_user
from apscheduler.triggers.cron import CronTrigger
from app import loginManager, sched
from app.models import *
from .my_schema import *
from .run_task import run_task
from common.response import ResMsg
from common.response_message import *
from common.return_list_page import list_page
from common.json_checker import format_checker

task = Blueprint('task', __name__)


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class TaskList(MethodView):
    """
    任务列表
    project_id是必填参数，获取project下的任务
    """
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(task_list_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        project_id = data.get('project_id')
        task_name = data.get('task_name') if data.get('task_name') is not None else ''
        page_num = data.get('page_num')
        page_size = data.get('page_size', 10)
        task_list = list()
        if project_id:
            try:
                tasks = Task.query.filter_by(project_id=project_id, status=True).filter(
                    Task.task_name.like('%' + task_name + '%')
                ).order_by(Task.id.desc()).all()
            except Exception as e:
                res.update(code=-1, data=str(e), msg=request_fail)
                return jsonify(res.data)
        else:
            try:
                tasks = Task.query.filter_by(status=True).filter(
                    Task.task_name.like('%' + task_name + '%')
                ).order_by(Task.id.desc()).all()
            except Exception as e:
                res.update(code=-1, data=str(e), msg=request_fail)
                return jsonify(res.data)
        if tasks:
            for t in tasks:
                project_name = t.projects.project_name if t.project_id else ''
                task_info = {
                    'task_id': t.id,
                    'task_name': t.task_name,
                    'task_type': t.task_type,
                    'run_status': t.run_status,
                    'case_num': t.interface.count(),
                    'project_name': project_name,
                    'create_user': t.users.username,
                }
                task_list.append(task_info)
        data, total = list_page(task_list, page_size, page_num)
        res.update(code=1, data=data, msg=request_success)
        res.add_field(name='page_total_num', value=total)
        return jsonify(res.data)


class TaskInfo(MethodView):
    """任务信息"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(task_info_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        task_id = data.get('task_id')
        exist_task = Task.query.filter_by(id=task_id, status=True).first()
        if not exist_task:
            res.update(code=-1, data='', msg=task_not_exist_error)
            return jsonify(res.data)
        if exist_task.s_uid == 0:
            s_user = ''
        else:
            start_user = User.query.get(exist_task.s_uid)
            s_user = start_user.username
        cases = exist_task.interface.all()
        case_list = list()
        if cases:
            for c in cases:
                case_info = {
                    'case_id': c.id,
                    'case_name': c.case_name,
                    'case_type': c.case_type,
                    'method': c.method,
                    'url': c.environments.url,
                    'path': c.path,
                    'project_name': c.projects.project_name if c.project_id else '',
                }
                case_list.append(case_info)
        task_info = {
            'task_id': task_id,
            'task_name': exist_task.task_name,
            'task_type': exist_task.task_type,
            'run_time': exist_task.run_time,
            'create_time': datetime.datetime.strftime(exist_task.create_time, "%Y-%m-%d %H:%M:%S"),
            'run_status': exist_task.run_status,
            'project_id': exist_task.project_id if exist_task.project_id else '',
            'project_name': exist_task.projects.project_name if exist_task.project_id else '',
            'create_user': exist_task.users.username,
            'start_user': s_user,
            'case_list': case_list,
        }
        res.update(code=1, data=task_info, msg=request_success)
        return jsonify(res.data)


class AddTask(MethodView):
    """新增任务"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(add_task_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        project_id = data.get('project_id')
        task_name = data.get('task_name')
        task_type = data.get('task_type')
        run_time = data.get('run_time')
        if task_type == 0:      # type=0时，立即执行
            run_time = ''
        elif task_type < 0 or task_type > 3:
            res.update(code=-1, data='', msg=task_type_not_exist_error)
            return jsonify(res.data)
        elif not run_time:
            res.update(code=-1, data='', msg=run_time_error)
            return jsonify(res.data)
        new_task = Task(
            task_name=task_name,
            task_type=task_type,
            run_time=run_time,
            project_id=project_id,
            c_uid=current_user.id
        )
        db.session.add(new_task)
        try:
            db.session.commit()
            task_info = {
                'task_id': new_task.id,
                'task_name': task_name,
            }
            res.update(code=1, data=task_info, msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class EditTask(MethodView):
    """编辑任务"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(edit_task_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        project_id = data.get('project_id')
        task_id = data.get('task_id')
        task_name = data.get('task_name')
        task_type = data.get('task_type')
        run_time = data.get('run_time')
        exist_task = Task.query.filter_by(id=task_id, status=True).first()
        if not exist_task:
            res.update(code=-1, data='', msg=task_not_exist_error)
            return jsonify(res.data)
        if exist_task.run_status == 1:
            res.update(code=-1, data='', msg=task_running_error)
            return jsonify(res.data)
        if task_type == 0:      # type=0时，立即执行
            run_time = ''
        elif task_type < 0 or task_type > 3:
            res.update(code=-1, data='', msg=task_type_not_exist_error)
            return jsonify(res.data)
        elif not run_time:
            res.update(code=-1, data='', msg=run_time_error)
            return jsonify(res.data)
        # elif task_type == 1:
        #     # ty = 'interval'   # type=1时，间隔秒数
        #     seconds = request.json.get('seconds')
        #     run_time = {'type': task_type, 'seconds': seconds}
        # elif task_type == 2:    # type=2时，时间string格式 '2020-04-02 19:00:00'
        #     # ty = 'date'
        #     run_date = request.json.get('run_date')
        #     run_time = {'type': task_type, 'run_date': run_date}
        # elif task_type == 3:    # type=3时，标准crontab格式'0 0 1-15 may-aug *'
        #     # ty = 'cron'
        #     cron_mes = request.json.get('cron_mes')
        #     run_time = {'type': task_type, 'cron_mes': cron_mes}
        # else:
        #     res.update(code=-1, data='', msg=task_type_not_exist_error)
        #     return jsonify(res.data)
        exist_task.task_name = task_name
        exist_task.task_type = task_type
        exist_task.run_time = run_time
        exist_task.project_id = project_id
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class DelTask(MethodView):
    """删除任务"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(task_info_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        task_id = data.get('task_id')
        exist_task = Task.query.filter_by(id=task_id, status=True).first()
        if not exist_task:
            res.update(code=-1, data='', msg=task_not_exist_error)
            return jsonify(res.data)
        if exist_task.run_status == 1:
            res.update(code=-1, data='', msg=task_running_error)
            return jsonify(res.data)
        exist_task.status = False
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class UpdateTaskCase(MethodView):
    """更新任务的用例信息"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(update_case_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        task_id = data.get('task_id')
        case_list = data.get('case_list')
        exist_task = Task.query.filter_by(id=task_id, status=True).first()
        if not exist_task:
            res.update(code=-1, data='', msg=task_not_exist_error)
            return jsonify(res.data)
        if exist_task.run_status == 1:
            res.update(code=-1, data='', msg=task_running_error)
            return jsonify(res.data)
        if len(case_list) > 10:     # 每个任务最多10个用例
            res.update(code=-1, data='', msg=case_count_limit_error)
            return jsonify(res.data)
        for oc in exist_task.interface.all():
            exist_task.interface.remove(oc)
        add_case_list = list()
        err_case_list = list()
        debug_case_list = list()
        if case_list:
            for case_id in case_list:
                exist_case = TestCase.query.filter_by(id=case_id, status=True).first()
                if exist_case:
                    if not exist_case.is_debug:
                        debug_case_list.append(case_id)
                        continue
                    add_case_list.append(case_id)
                    exist_task.interface.append(exist_case)
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
            res.update(code=1, data=case_info, msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class StartTask(MethodView):
    """启动任务"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(task_info_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        task_id = data.get('task_id')
        exist_task = Task.query.filter_by(id=task_id, status=True).first()
        if not exist_task:
            res.update(code=-1, data='', msg=task_not_exist_error)
            return jsonify(res.data)
        if len(exist_task.interface.all()) == 0:
            res.update(code=-1, data='', msg=task_case_not_exist_error)
            return jsonify(res.data)
        if exist_task.run_status == 1:
            res.update(code=-1, data='', msg=task_running_error)
            return jsonify(res.data)
        task_type = exist_task.task_type
        run_time = exist_task.run_time
        job_name = '%s_%d' % (exist_task.task_name, task_id)
        uid = current_user.id
        try:
            if task_type == 0:      # type=0时，立即执行
                run_task(task_id, uid)
            elif task_type == 1:    # type=1时，间隔秒数
                sched.add_job(run_task, 'interval', seconds=int(run_time), id=job_name, args=[str(task_id), uid],
                              jobstore='redis', replace_existing=True)
            elif task_type == 2:    # type=2时，时间string格式 '2020-04-02 19:00:00'
                sched.add_job(run_task, 'date', run_date=run_time, id=job_name, args=[str(task_id), uid],
                              jobstore='redis', replace_existing=True)
            elif task_type == 3:    # type=3时，标准crontab格式'0 0 1-15 may-aug *'
                sched.add_job(run_task, CronTrigger.from_crontab(run_time), id=job_name, args=[str(task_id), uid],
                              jobstore='redis', replace_existing=True)
        except Exception as e:
            res.update(code=-1, data=str(e), msg=task_start_error)
            return jsonify(res.data)
        exist_task.run_status = 1
        exist_task.s_uid = uid
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class StopTask(MethodView):
    """停止任务"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(task_info_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        task_id = data.get('task_id')
        exist_task = Task.query.filter_by(id=task_id, status=True).first()
        if not exist_task:
            res.update(code=-1, data='', msg=task_not_exist_error)
            return jsonify(res.data)
        if exist_task.task_type != 0:
            job_name = '%s_%d' % (exist_task.task_name, task_id)
            if sched.get_job(job_name):
                sched.remove_job(job_name)
            else:
                mes = {job_name: '缓存中没有该任务信息'}
                res.update(code=-1, data=mes, msg=task_stop_error)
                return jsonify(res.data)
        exist_task.run_status = 2
        try:
            db.session.commit()
            res.update(code=1, data='', msg=request_success)
            return jsonify(res.data)
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)


class TaskResList(MethodView):
    """任务执行结果列表"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(task_res_list_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        task_id = data.get('task_id')
        page_num = data.get('page_num')
        page_size = data.get('page_size', 10)
        task_res_list = list()
        exist_task = Task.query.filter_by(id=task_id, status=True).first()
        if not exist_task:
            res.update(code=-1, data='', msg=task_not_exist_error)
            return jsonify(res.data)
        try:
            task_results = TestResult.query.filter_by(task_id=task_id).order_by(TestResult.id.desc()).all()
        except Exception as e:
            res.update(code=-1, data=str(e), msg=request_fail)
            return jsonify(res.data)
        if task_results:
            for tr in task_results:
                task_info = {
                    'task_result_id': tr.id,
                    'case_num': tr.case_num,
                    'pass_num': tr.pass_num,
                    'fail_num': tr.fail_num,
                    'exception_num': tr.exception_num,
                    'start_time': datetime.datetime.strftime(tr.start_time, "%Y-%m-%d %H:%M:%S"),
                    'duration': tr.duration,
                }
                task_res_list.append(task_info)
        data, total = list_page(task_res_list, page_size, page_num)
        res.update(code=1, data=data, msg=request_success)
        res.add_field(name='page_total_num', value=total)
        return jsonify(res.data)


class TaskResInfo(MethodView):
    """任务执行结果详情"""
    @login_required
    def post(self):
        res = ResMsg()
        data = request.get_json()
        flag, mes = format_checker(task_res_info_schema, data)
        if not flag:
            res.update(code=-1, data=mes, msg=param_format_error)
            return jsonify(res.data)
        task_result_id = data.get('task_result_id')
        task_result = TestResult.query.filter_by(id=task_result_id).first()
        if not task_result:
            res.update(code=-1, data='', msg=task_res_not_exist_error)
            return jsonify(res.data)
        exist_task = Task.query.filter_by(id=task_result.task_id, status=True).first()
        if not exist_task:
            res.update(code=-1, data='', msg=task_not_exist_error)
            return jsonify(res.data)
        task_info = {
            'task_result_id': task_result.id,
            'task_name': exist_task.task_name,
            'case_num': task_result.case_num,
            'pass_num': task_result.pass_num,
            'fail_num': task_result.fail_num,
            'exception_num': task_result.exception_num,
            'start_time': datetime.datetime.strftime(task_result.start_time, "%Y-%m-%d %H:%M:%S"),
            'duration': task_result.duration,
            'test_report': task_result.test_report,
            'test_log': task_result.test_log,
        }
        res.update(code=1, data=task_info, msg=request_success)
        return jsonify(res.data)
