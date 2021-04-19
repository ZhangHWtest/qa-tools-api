# -*- coding: utf-8 -*-

import os
import time
import json
from app.models import *
from common.aksk_sign import make_aksk_sign
from common.requ_case import ApiRequest
from common.my_db import *
from common.get_value import get_value_from_dict
from common.panduan import assert_contain
from common.log import MyLogger


class RunCase(object):
    def __init__(self, task_id=None, log_mes=None):
        self.task_id = task_id
        if log_mes is None:
            day = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
            file_name = 'runcase_%s' % day
            cur_path = os.getcwd()
            file_dir = cur_path + '/app/upload'
            log_file = os.path.join(file_dir, (file_name + '.log'))
            self.log_mes = MyLogger(u'测试日志', filename=log_file).get_both_logger()
        else:
            self.log_mes = log_mes
        self.session = None
        self.global_params = dict()

    def run_single_case(self, case_id):
        result = {
            'case_id': case_id,
            'case_name': '',
            'case_type': '',
            'case_method': '',
            'case_path': '',
            'case_params': {},
            'input_para_info': {},
            'case_header': {},
            'input_header_info': {},
            'aksk_header_info': {},
            'case_assert': {},
            'case_result': '',
            'case_resp': {},
            'output_para_info': {},
            'case_diff': {},
            'case_spend': 0,
            'result_except': 0,
            'result_fail': 0,
            'result_pass': 0,
            'task_id': self.task_id,
            'environment': None,
        }
        self.log_mes.info('用例：%d 开始执行' % case_id)
        case = TestCase.query.get(case_id)
        if not case:
            self.log_mes.error('用例：%d 执行失败！用例不存在' % case_id)
            result['case_result'] = 2   # 0失败，1通过，2异常
            result['case_resp'] = {'exception': '用例不存在，执行失败'}
            result['case_spend'] = -1
            result['result_except'] = 1
            return result
        if case.status is False:
            self.log_mes.error('用例：%d 执行失败！用例已删除' % case_id)
            result['case_result'] = 2   # 0失败，1通过，2异常
            result['case_resp'] = {'exception': '用例已删除，执行失败'}
            result['case_spend'] = -1
            result['result_except'] = 1
            return result
        method = case.method
        str_params = case.params
        str_header = case.header
        input_para_info, input_header_info, input_info, output_para_info = ['', '', '', '']
        has_input = case.has_input
        if has_input == 1:
            self.log_mes.info('用例：%d 需要入参' % case_id)
            input_para = case.input_para
            if input_para:
                input_para_info = dict()
                ip_list = input_para.split(',')
                for ip in ip_list:
                    ipv = get_value_from_dict(self.global_params, ip)
                    para = '${%s}' % ip
                    if para in str_params:
                        str_params = str_params.replace(para, ipv)
                    else:
                        self.log_mes.error('用例：%d 执行失败！用例参数 %s 入参失败' % (case_id, para))
                        result['case_result'] = 2  # 0失败，1通过，2异常
                        result['case_resp'] = {'exception': '用例参数 %s 入参失败，执行失败' % para}
                        result['case_spend'] = -1
                        result['result_except'] = 1
                        return result
                    input_para_info[ip] = ipv
            input_header = case.input_header
            if input_header:
                input_header_info = dict()
                ih_list = input_header.split(',')
                for ih in ih_list:
                    ihv = get_value_from_dict(self.global_params, ih)
                    head = '${%s}' % ih
                    if head in str_header:
                        str_header = str_header.replace(head, ihv)
                    else:
                        self.log_mes.error('用例：%d 执行失败！用例header参数 %s 入参失败' % (case_id, head))
                        result['case_result'] = 2  # 0失败，1通过，2异常
                        result['case_resp'] = {'exception': '用例header参数 %s 入参失败，执行失败' % head}
                        result['case_spend'] = -1
                        result['result_except'] = 1
                        return result
                    input_header_info[ih] = ihv
            input_info = {
                'input_para': input_para_info,
                'input_header': input_header_info
            }
            self.log_mes.info('用例：%d 入参信息为 %s' % (case_id, json.dumps(input_info, ensure_ascii=False)))
        params = json.loads(str_params)
        header = json.loads(str_header)
        res_assert = json.loads(case.res_assert)
        save_result = case.save_result
        use_db = case.use_db
        result['case_name'] = case.case_name
        result['case_type'] = case.case_type
        result['case_method'] = method
        result['case_params'] = params
        result['input_para_info'] = input_para_info
        result['case_header'] = header
        result['input_header_info'] = input_header_info
        result['case_assert'] = res_assert
        result['environment'] = case.env_id
        exist_env = Environment.query.filter_by(id=case.env_id, status=True).first()
        if not exist_env:
            self.log_mes.error('用例：%d 执行失败！测试环境 %d 不存在' % (case_id, case.env_id))
            result['case_result'] = 2   # 0失败，1通过，2异常
            result['case_resp'] = {'exception': '当前用例测试环境不存在，执行失败'}
            result['case_spend'] = -1
            result['result_except'] = 1
            self.save_case_result(result, save_result)
            return result
        path = exist_env.url + case.path
        result['case_path'] = path
        rely_cases = case.rely_case.all()
        if rely_cases:  # 执行依赖用例，加入依赖参数的key,value
            rely_param_list = json.loads(case.rely_params)
            for x in range(len(rely_cases)):
                rely_case_id = rely_cases[x].id
                self.log_mes.info('****** 用例：%d 开始执行依赖用例：%d ******' % (case_id, rely_case_id))
                res = self.run_single_case(rely_case_id)
                rely_param = rely_param_list[x]
                rely_param_value = get_value_from_dict(res['case_resp'], rely_param)
                if rely_param_value is None:
                    self.log_mes.error('用例：%d 执行失败！依赖用例 %d 的参数 %s 为空' % (case_id, rely_case_id, rely_param))
                    result['case_result'] = 2   # 0失败，1通过，2异常
                    result['case_resp'] = {'exception': '依赖用例 %d 的参数 %s 为空，执行失败' % (rely_case_id, rely_param)}
                    result['case_spend'] = -1
                    result['result_except'] = 1
                    self.save_case_result(result, save_result)
                    return result
                params.update({rely_param: rely_param_value})
                self.log_mes.info('****** 用例：%d 的依赖用例：%d 执行成功 ******' % (case_id, rely_case_id))
            result['case_params'] = params
        has_sign = case.has_sign
        if has_sign == 1:
            self.log_mes.info('用例：%d 需要AKSK签名认证' % case_id)
            ak = case.ak
            sk = case.sk
            aksk_header = make_aksk_sign(ak, sk, params)
            header.update(aksk_header)
            result['case_header'] = header
            result['aksk_header_info'] = aksk_header
        try:
            self.log_mes.info('==== 用例：%d 开始请求接口 %s ====' % (case_id, path))
            api = ApiRequest(url=path, method=method, params=params, headers=header, session=self.session)
            resp, spend = api.test_api()
            self.session = api.get_session()
            self.log_mes.info('==== 用例：%d 接口请求完成，耗时 %s ====' % (case_id, str(spend)))
        except Exception as e:
            self.log_mes.error('用例：%d 执行异常！错误信息：%s' % (case_id, str(e)))
            result['case_result'] = 2   # 0失败，1通过，2异常
            result['case_resp'] = {'exception': '当前用例执行失败，错误信息：%s' % str(e)}
            result['case_spend'] = -1
            result['result_except'] = 1
            self.save_case_result(result, save_result)
            return result
        has_output = case.has_output
        if has_output == 1:
            self.log_mes.info('用例：%d 需要出参' % case_id)
            output_para = case.output_para
            output_para_info = dict()
            op_list = output_para.split(',')
            for op in op_list:
                opv = get_value_from_dict(resp, op)
                output_para_info[op] = opv
            self.global_params.update(output_para_info)
            self.log_mes.info('用例：%d 出参信息为 %s' % (case_id, json.dumps(output_para_info, ensure_ascii=False)))
            self.log_mes.info('当前公共参数信息为 %s' % json.dumps(self.global_params, ensure_ascii=False))
        result['output_para_info'] = output_para_info
        if use_db:
            sql = case.sql
            field_value = case.field_value
            field_list = field_value.split(',')
            if not exist_env.use_db:
                self.log_mes.error('用例：%d 执行失败！测试环境 %d 没有配置数据库信息' % (case_id, case.env_id))
                result['case_result'] = 2  # 0失败，1通过，2异常
                result['case_resp'] = {'exception': '当前用例测试环境没有配置数据库信息，执行失败'}
                result['case_spend'] = -1
                result['result_except'] = 1
                self.save_case_result(result, save_result)
                return result
            con = curse_db(exist_env.db_host, exist_env.db_port, exist_env.db_user,
                           exist_env.db_pass, exist_env.database)
            if con['code'] != 1:
                self.log_mes.error('用例：%d 执行失败！测试环境 %d 连接数据库错误 %s' % (case_id, case.env_id, con['error']))
                result['case_result'] = 2  # 0失败，1通过，2异常
                result['case_resp'] = {'exception': '当前用例测试环境连接数据库错误，执行失败'}
                result['case_spend'] = -1
                result['result_except'] = 1
                self.save_case_result(result, save_result)
                return result
            sql_res = execute_mysql(con, sql)
            if sql_res['code'] != 1:
                self.log_mes.error('用例：%d 执行失败！测试环境 %d 执行sql语句错误 %s' % (case_id, case.env_id, sql_res['error']))
                result['case_result'] = 2  # 0失败，1通过，2异常
                result['case_resp'] = {'exception': '当前用例测试环境执行sql语句错误，执行失败'}
                result['case_spend'] = -1
                result['result_except'] = 1
                self.save_case_result(result, save_result)
                return result
            res_list = sql_res['result']
            if len(field_list) == len(sql_res):
                resp = dict(zip(field_list, res_list))
            else:
                self.log_mes.error('用例：%d 执行失败！数据库校验字段 %s 和sql取值 %s 对应关系错误'
                                   % (case_id, field_value, ','.join(sql_res)))
                result['case_result'] = 2  # 0失败，1通过，2异常
                result['case_resp'] = {'exception': '数据库校验字段 %s 和sql取值 %s 对应关系错误，执行失败'
                                                    % (field_value, ','.join(sql_res))}
                result['case_spend'] = -1
                result['result_except'] = 1
                self.save_case_result(result, save_result)
                return result
        diff_res = assert_contain(res_assert, resp)
        result['case_resp'] = resp
        result['case_diff'] = diff_res
        result['case_spend'] = spend
        if diff_res:
            self.log_mes.info('用例 %d 执行完成，未通过，有问题数据为 %s' % (case_id, json.dumps(diff_res, ensure_ascii=False)))
            result['case_result'] = 0   # 0失败，1通过，2异常
            result['result_fail'] = 1
        else:
            self.log_mes.info('用例 %d 执行完成，通过' % case_id)
            result['case_result'] = 1  # 0失败，1通过，2异常
            result['result_pass'] = 1
        self.save_case_result(result, save_result)
        return result

    def save_case_result(self, result_dic, save_result):
        if save_result:
            try:
                new_case_res = CaseResult(
                    case_type=result_dic['case_type'],
                    method=result_dic['case_method'],
                    path=result_dic['case_path'],
                    params=json.dumps(result_dic['case_params'], ensure_ascii=False),
                    input_para=json.dumps(result_dic['input_para_info'], ensure_ascii=False),
                    header=json.dumps(result_dic['case_header'], ensure_ascii=False),
                    input_header=json.dumps(result_dic['input_header_info'], ensure_ascii=False),
                    aksk_header=json.dumps(result_dic['aksk_header_info'], ensure_ascii=False),
                    res_assert=json.dumps(result_dic['case_assert'], ensure_ascii=False),
                    case_result=result_dic['case_result'],
                    response=json.dumps(result_dic['case_resp'], ensure_ascii=False),
                    output_para=json.dumps(result_dic['output_para_info'], ensure_ascii=False),
                    diff_res=json.dumps(result_dic['case_diff'], ensure_ascii=False),
                    duration=result_dic['case_spend'],
                    case_id=result_dic['case_id'],
                    task_id=result_dic['task_id'],
                    environment=result_dic['environment']
                )
                db.session.add(new_case_res)
                db.session.commit()
                self.log_mes.info('用例 %d 执行信息入库成功' % result_dic['case_id'])
            except Exception as e:
                db.session.rollback()
                self.log_mes.error('用例 %d 执行信息入库失败！错误信息：%s' % (result_dic['case_id'], str(e)))
        else:
            self.log_mes.info('用例 %d 设置为不保存执行结果' % result_dic['case_id'])
