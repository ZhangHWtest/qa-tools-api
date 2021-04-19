# -*- coding: utf-8 -*-

import os
import time
import json
from app.models import *
from common.requ_case import ApiRequest
from common.get_value import get_value_from_dict, mma_list
from common.panduan import assert_contain
from common.report_html import generate_report
from common.log import MyLogger


def run_task(task_id, day=None):  # 定时任务执行的时候所用的函数
    task_id = int(task_id)
    exist_task = Task.query.filter_by(id=task_id, status=True).first()
    start_time = datetime.datetime.now()
    st = time.time()
    if not day:
        day = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
    file_name = 'task%.6d_%s' % (task_id, day)
    cur_path = os.getcwd()
    file_dir = cur_path + '/app/upload'
    log_file = os.path.join(file_dir, (file_name + '.log'))
    log_mes = MyLogger(u'测试日志', filename=log_file)
    # if os.path.exists(log_file) is False:
    #     os.system('touch %s' % log_file)
    rep_file = os.path.join(file_dir, (file_name + '.html'))
    # if os.path.exists(rep_file) is False:
    #     os.system(r'touch %s' % rep_file)
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
    log_mes.info_log('任务：%d 开始执行' % task_id)
    for case in exist_task.interface.all():
        case_id = case.id
        case_id_list.append(case_id)
        case_name = case.case_name
        case_name_list.append(case_name)
        method = case.method
        case_method_list.append(method)
        log_mes.info_log('用例：%d 开始执行' % case_id)
        if case.status is False:
            log_mes.error_log('用例：%d 执行失败！用例已删除' % case_id)
            case_path_list.append('')
            case_params_list.append('')
            case_header_list.append('')
            case_assert_list.append('')
            case_result_list.append(2)  # 0失败，1通过，2异常
            resp_list.append('当前用例已删除，执行失败')
            diff_list.append('')
            spend_list.append(-1)
            result_except += 1
            continue
        exist_env = Environment.query.filter_by(id=case.env_id, status=True).first()
        if not exist_env:
            log_mes.error_log('用例：%d 执行失败！测试环境不存在' % case_id)
            case_path_list.append('')
            case_params_list.append('')
            case_header_list.append('')
            case_assert_list.append('')
            case_result_list.append(2)  # 0失败，1通过，2异常
            resp_list.append('当前用例测试环境不存在，执行失败')
            diff_list.append('')
            spend_list.append(-1)
            result_except += 1
            continue
        path = exist_env.url + case.path
        case_path_list.append(path)
        case_header_list.append(case.header)
        case_assert_list.append(case.res_assert)
        params = json.loads(case.params)
        header = json.loads(case.header)
        res_assert = json.loads(case.res_assert)
        rely_cases = case.rely_case.all()
        if rely_cases:  # 执行依赖用例，加入依赖参数的key,value
            rely_param_list = json.loads(case.rely_params)
            for x in range(len(rely_cases)):
                rely_case_id = rely_cases[x].id
                rely_case = TestCase.query.filter_by(id=rely_case_id, status=True).first()
                if not rely_case:
                    log_mes.error_log('用例：%d 执行失败！依赖用例 %d 已删除' % (case_id, rely_case_id))
                    case_params_list.append(case.params)
                    case_result_list.append(2)  # 0失败，1通过，2异常
                    resp_list.append('依赖用例 %d 已删除，执行失败' % rely_case_id)
                    diff_list.append('')
                    spend_list.append(-1)
                    result_except += 1
                    continue
                rc_env = Environment.query.filter_by(id=rely_case.env_id, status=True).first()
                if not rc_env:
                    log_mes.error_log('用例：%d 执行失败！依赖用例 %d 的测试环境 %d 不存在'
                                      % (case_id, rely_case_id, rely_case.env_id))
                    case_params_list.append(case.params)
                    case_result_list.append(2)  # 0失败，1通过，2异常
                    resp_list.append('依赖用例 %d 的测试环境不存在，执行失败' % rely_case_id)
                    diff_list.append('')
                    spend_list.append(-1)
                    result_except += 1
                    continue
                try:
                    api = ApiRequest(
                        url=rc_env.url + rely_case.path,
                        method=rely_case.method,
                        params=json.loads(rely_case.params) if rely_case.params else '',
                        headers=json.loads(rely_case.header) if rely_case.header else ''
                    )
                    r, s = api.test_api()
                except Exception as e:
                    log_mes.error_log('用例：%d 执行异常！依赖用例 %d 执行失败，错误信息：%s'
                                      % (case_id, rely_case_id, str(e)))
                    case_params_list.append(case.params)
                    case_result_list.append(2)  # 0失败，1通过，2异常
                    resp_list.append('依赖用例 %d 执行失败，错误信息：%s' % (rely_case_id, str(e)))
                    diff_list.append('')
                    spend_list.append(-1)
                    result_except += 1
                    continue
                rely_param = rely_param_list[x]
                rely_param_value = get_value_from_dict(r, rely_param)
                if rely_param_value is None:
                    log_mes.error_log('用例：%d 执行失败！依赖用例 %s 的参数 %s 为空'
                                      % (case_id, rely_case_id, rely_param))
                    case_params_list.append(case.params)
                    case_result_list.append(2)  # 0失败，1通过，2异常
                    resp_list.append('依赖用例 %d 的参数 %s 为空，执行失败' % (rely_case_id, rely_param))
                    diff_list.append('')
                    spend_list.append(-1)
                    result_except += 1
                    continue
                params.update({rely_param: rely_param_value})
        case_params_list.append(json.dumps(params, ensure_ascii=False))
        try:
            api = ApiRequest(url=path, method=method, params=params, headers=header)
            result, spend = api.test_api()
        except Exception as e:
            log_mes.error_log('用例：%d 执行异常！错误信息：%s' % (case_id, str(e)))
            case_result_list.append(2)  # 0失败，1通过，2异常
            resp_list.append('当前用例执行失败，错误信息：%s' % str(e))
            diff_list.append('')
            spend_list.append(-1)
            result_except += 1
            continue
        diff_res = assert_contain(res_assert, result)
        resp_list.append(json.dumps(result, ensure_ascii=False))
        diff_list.append(json.dumps(diff_res, ensure_ascii=False))
        spend_list.append(spend)
        if diff_res:
            log_mes.info_log('用例 %d 执行完成，未通过，有问题数据为 %s' % (case_id, json.dumps(diff_res, ensure_ascii=False)))
            case_result_list.append(0)  # 0失败，1通过，2异常
            result_fail += 1
        else:
            log_mes.info_log('用例 %d 执行完成，通过' % case_id)
            case_result_list.append(1)  # 0失败，1通过，2异常
            result_pass += 1
    end_time = datetime.datetime.now()
    et = time.time()
    case_total = len(case_id_list)
    ma, mi, avg = mma_list(spend_list)
    generate_report(filepath=rep_file, tit=u'定时任务接口测试报告', st=start_time, et=end_time, passes=result_pass,
                    fails=result_fail, excepts=result_except, cid=case_id_list, cname=case_name_list,
                    method_list=case_method_list, path_list=case_path_list, params_list=case_params_list,
                    header_list=case_header_list, assert_list=case_assert_list, resp_list=resp_list,
                    result_list=case_result_list, maxi=ma, mini=mi, aver=avg)
    log_mes.info_log('任务 %d 用例执行完成，生成测试报告 %s' % (task_id, rep_file))
    for i in range(len(case_id_list)):
        case = TestCase.query.filter_by(id=case_id_list[i]).first()
        new_case_res = CaseResult(
            case_type=case.case_type,
            method=case_method_list[i],
            path=case_path_list[i],
            params=case_params_list[i],
            header=case_header_list[i],
            res_assert=case_assert_list[i],
            case_result=case_result_list[i],
            response=resp_list[i],
            diff_res=diff_list[i],
            duration=spend_list[i],
            case_id=case_id_list[i],
            task_id=task_id,
            environment=case.env_id
        )
        db.session.add(new_case_res)
    duration = et - st
    new_task_res = TestResult(
        case_num=case_total,
        pass_num=result_pass,
        fail_num=result_fail,
        exception_num=result_except,
        start_time=start_time,
        duration=duration,
        test_report=rep_file,
        test_log=log_file,
        c_uid=1,
        projects_id=exist_task.project_id,
        task_id=exist_task.id,
    )
    db.session.add(new_task_res)
    try:
        db.session.commit()
        log_mes.info_log('任务 %d 执行信息入库成功' % task_id)
    except Exception as e:
        db.session.rollback()
        log_mes.error_log('任务 %d 执行信息入库失败！错误信息：%s' % (task_id, str(e)))
