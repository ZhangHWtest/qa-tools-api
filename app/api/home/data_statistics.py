# -*- coding: utf-8 -*-

import os
from sqlalchemy import extract, and_
from app.models import *
from common.pyredis import MyRedis
from common.log import MyLogger


def get_yesterday(day):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=day)
    return yesterday


def case_data_statistics(day=1, save=True, path=None):
    """统计前n天（默认1）接口、用例的执行情况，并存入CaseStatistics表"""
    open_date = get_yesterday(day)
    day = str(open_date)
    file_name = 'case_statistics.log'
    if not path:
        cur_path = os.getcwd()
        file_dir = cur_path + '/app/upload'
        log_file = os.path.join(file_dir, file_name)
    else:
        log_file = os.path.join('.../upload', file_name)
    log_mes = MyLogger(u'每日用例统计日志', filename=log_file).get_file_logger()
    log_mes.info('~~~~~~~~~~ 开始统计昨天 %s 用例执行数据 ~~~~~~~~~~' % day)
    if not MyRedis().check_redis_lock('cds', 'lock', 10):
        log_mes.info('检查发现已有任务执行，统计结束')
        data = {'Exception': '检查发现已有任务执行，统计结束'}
        return data
    interface_num = Interface.query.filter_by(status=True).count()
    log_mes.info('interface_num = %d' % interface_num)
    cases = TestCase.query.filter_by(status=True)
    case_num = cases.count()
    log_mes.info('case_num = %d' % case_num)
    run_case_res = CaseResult.query.filter()
    run_case_num = run_case_res.count()
    failure_case_num = run_case_res.filter_by(case_result=0).count()
    success_case_num = run_case_res.filter_by(case_result=1).count()
    exception_case_num = run_case_res.filter_by(case_result=2).count()
    today_run_case_res = run_case_res.filter(and_(
        extract("year", CaseResult.start_time) == open_date.year,
        extract("month", CaseResult.start_time) == open_date.month,
        extract("day", CaseResult.start_time) == open_date.day
    ))
    today_run_case_num = today_run_case_res.count()
    today_fail_case_num = today_run_case_res.filter_by(case_result=0).count()
    today_suc_case_num = today_run_case_res.filter_by(case_result=1).count()
    today_exc_case_num = today_run_case_res.filter_by(case_result=2).count()
    data = {
        'interface_num': interface_num,
        'case_num': case_num,
        'run_case_num': run_case_num,
        'success_case_num': success_case_num,
        'failure_case_num': failure_case_num,
        'exception_case_num': exception_case_num,
        'today_run_case_num': today_run_case_num,
        'today_suc_case_num': today_suc_case_num,
        'today_fail_case_num': today_fail_case_num,
        'today_exc_case_num': today_exc_case_num,
        'open_date': day,
    }
    log_mes.info('用例执行数据统计完成： %s' % str(data))
    cs = CaseStatistics.query.filter().order_by(CaseStatistics.id.desc()).first()
    d1 = datetime.datetime.strptime(day, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(cs.open_date, '%Y-%m-%d')
    if d1 <= d2:
        log_mes.info('用例数据统计表最后一条数据日期是 %s，统计日期异常，结束统计' % cs.open_date)
        data['Exception'] = '用例数据统计表最后一条数据日期是 %s，统计日期异常，结束统计' % cs.open_date
        return data
    new_case_statistics = CaseStatistics(
        interface_num=interface_num,
        case_num=case_num,
        run_case_num=run_case_num,
        success_case_num=success_case_num,
        failure_case_num=failure_case_num,
        exception_case_num=exception_case_num,
        today_run_case_num=today_run_case_num,
        today_suc_case_num=today_suc_case_num,
        today_fail_case_num=today_fail_case_num,
        today_exc_case_num=today_exc_case_num,
        open_date=day,
    )
    if save:
        db.session.add(new_case_statistics)
        try:
            db.session.commit()
            log_mes.info('用例统计数据入库成功')
        except Exception as e:
            db.session.rollback()
            data['Exception'] = str(e)
            log_mes.error('用例统计数据入库失败，异常信息：%s' % str(e))
    return data


if __name__ == '__main__':
    r = case_data_statistics(1, False, 1)
    print(r)
