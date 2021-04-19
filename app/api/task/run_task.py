# -*- coding: utf-8 -*-

import os
import time
import json
from app.models import *
from common.pyredis import MyRedis
from common.get_value import mma_list
from common.report_html import generate_report
from common.log import MyLogger
from ..case.run_case import RunCase


def run_task(task_id, uid, day=None):  # 定时任务执行的时候所用的函数
    task_id = int(task_id)
    exist_task = Task.query.filter_by(id=task_id, status=True).first()
    start_time = datetime.datetime.now()
    st = time.time()
    if not day:
        day = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
    file_name = 'task%.6d_%s' % (task_id, day)
    lf = file_name + '.log'
    rf = file_name + '.html'
    cur_path = os.getcwd()
    file_dir = cur_path + '/app/upload'
    log_file = os.path.join(file_dir, lf)
    log_mes = MyLogger(u'测试日志', filename=log_file).get_both_logger()
    rep_file = os.path.join(file_dir, rf)
    run_case = RunCase(task_id, log_mes)
    case_id_list = list()
    case_name_list = list()
    case_method_list = list()
    case_path_list = list()
    case_params_list = list()
    case_header_list = list()
    case_assert_list = list()
    case_result_list = list()
    resp_list = list()
    diff_list = list()
    spend_list = list()
    result_pass = 0
    result_fail = 0
    result_except = 0
    unknown = 0
    log_mes.info('任务：%d 开始执行' % task_id)
    if not MyRedis().check_redis_lock('run_task', '1', 2):
        log_mes.info('检查发现已有任务执行，任务终止')
        data = {'Exception': '检查发现已有任务执行，任务终止'}
        return data
    for case in exist_task.interface.all():
        result = run_case.run_single_case(case.id)
        case_id_list.append(result['case_id'])
        case_name_list.append(result['case_name'])
        case_method_list.append(result['case_method'])
        case_path_list.append(result['case_path'])
        case_params_list.append(json.dumps(result['case_params'], ensure_ascii=False))
        case_header_list.append(json.dumps(result['case_header'], ensure_ascii=False))
        case_assert_list.append(json.dumps(result['case_assert'], ensure_ascii=False))
        case_result_list.append(result['case_result'])
        resp_list.append(json.dumps(result['case_resp'], ensure_ascii=False))
        diff_list.append(json.dumps(result['case_diff'], ensure_ascii=False))
        spend_list.append(result['case_spend'])
        if result['case_result'] == 0:
            result_fail += 1
        elif result['case_result'] == 1:
            result_pass += 1
        elif result['case_result'] == 2:
            result_except += 1
        else:
            unknown += 1
    end_time = datetime.datetime.now()
    et = time.time()
    case_total = len(case_id_list)
    ma, mi, avg = mma_list(spend_list)
    generate_report(filepath=rep_file, tit=u'定时任务接口测试报告', st=start_time, et=end_time, passes=result_pass,
                    fails=result_fail, excepts=result_except, unknown=unknown, cid=case_id_list, cname=case_name_list,
                    method_list=case_method_list, path_list=case_path_list, params_list=case_params_list,
                    header_list=case_header_list, assert_list=case_assert_list, resp_list=resp_list,
                    result_list=case_result_list, maxi=ma, mini=mi, aver=avg)
    log_mes.info('任务 %d 用例执行完成，生成测试报告 %s' % (task_id, rep_file))
    duration = et - st
    new_task_res = TestResult(
        case_num=case_total,
        pass_num=result_pass,
        fail_num=result_fail,
        exception_num=result_except,
        unknown_num=unknown,
        start_time=start_time,
        duration=duration,
        test_report=rf,
        test_log=lf,
        c_uid=uid,
        projects_id=exist_task.project_id,
        task_id=exist_task.id,
    )
    db.session.add(new_task_res)
    try:
        db.session.commit()
        log_mes.info('任务 %d 执行信息入库成功' % task_id)
    except Exception as e:
        db.session.rollback()
        log_mes.error('任务 %d 执行信息入库失败！错误信息：%s' % (task_id, str(e)))
