# -*- coding: utf-8 -*-

import os
import json
import platform
from common.get_value import get_data_from_postman_json


class ImportJson(object):
    """从json文件中导入各种格式的接口数据，输出统一格式的接口数据"""
    def __init__(self, file_name):
        """根据上传文件名初始化上传文件路径"""
        cur_path = os.getcwd()
        systype = platform.system()
        if systype == "Windows":  # windows系统参数
            file_dir = cur_path + '\\app\\upload'
        elif systype == "Linux":  # linux系统参数
            file_dir = cur_path + '/app/upload'
        else:
            file_dir = cur_path
        self.upload_file = os.path.join(file_dir, (file_name + '.json'))

    def get_data_list(self, json_type):
        """根据上传json文件的不同格式，调用不同方法导入json数据并输出统一接口数据"""
        try:
            f = open(self.upload_file, 'r+', encoding='UTF-8')
            str_json = f.read()
            json_list = json.loads(str_json)
        except Exception as e:
            return -1, e
        if json_type == 'yapi':
            data_list = self.import_yapi_json_data(json_list)
        elif json_type == 'postman':
            data_list = self.import_postman_json_data(json_list)
        else:
            data_list = []
        return 1, data_list

    def import_yapi_json_data(self, yapi_data):
        """导入yapi平台接口数据的json文件"""
        data_list = []
        for json_data in yapi_data:
            interface_list = json_data['list']
            for interface_data in interface_list:
                interface_name = interface_data['title']
                interface_desc = interface_data['desc']
                if len(interface_desc) > 60:
                    interface_desc = ''
                interface_type = 'http'
                method = interface_data['method']
                path = interface_data['path']
                header_list = interface_data['req_headers']
                if len(header_list) > 0:
                    head = dict()
                    for h in header_list:
                        head[h['name']] = h['value']
                    header = json.dumps(head, ensure_ascii=False)
                else:
                    header = ''
                response = interface_data['res_body']
                params_list = []
                if method == 'GET' or method == 'get':
                    p_list = interface_data['req_query']
                elif method == 'POST' or method == 'post':
                    p_list = interface_data['req_body_form']
                else:
                    p_list = []
                if p_list:
                    for p in p_list:
                        p_data = {
                            'param_name': p['name'],
                            'param_desc': p['desc'],
                            'necessary': True if p.get('required') == '1' else False,
                            'default': p['example'],
                        }
                        params_list.append(p_data)
                new_data = {
                    'interface_name': interface_name,
                    'interface_desc': interface_desc,
                    'interface_type': interface_type,
                    'method': method,
                    'path': path,
                    'header': header,
                    'params': params_list,
                    'response': response,
                }
                data_list.append(new_data)
        return data_list

    def import_postman_json_data(self, postman_data):
        """导入postman工具接口数据的json文件"""
        data_list, json_list = [[], []]
        json_list = get_data_from_postman_json(postman_data, 'item', json_list)
        for item_data in json_list:
            interface_name = item_data['name']
            interface_data = item_data['request']
            method = interface_data['method']
            interface_desc = interface_data['description']
            if len(interface_desc) > 60:
                interface_desc = ''
            url = interface_data['url']
            i_type = url.get('protocol')
            if i_type is None:
                interface_type = 'http'
            elif i_type == 'http' or i_type == 'https':
                interface_type = i_type
            else:
                continue    # 不支持非http/https协议，直接忽略接口信息
            i_path = url.get('path')
            if i_path is None:
                path = '/'
            else:
                path = ''
                for p in i_path:
                    path = path + '/' + p
            header_list = interface_data['header']
            if len(header_list) > 0:
                head = dict()
                for h in header_list:
                    head[h['key']] = h['value']
                header = json.dumps(head, ensure_ascii=False)
            else:
                header = ''
            params_list = []
            if method == 'GET':
                p_list = url.get('query')
                if p_list:
                    for p in p_list:
                        p_data = {
                            'param_name': p['key'],
                            'param_desc': p['description'],
                            'necessary': True if p.get('disabled') else False,
                            'default': p['value'],
                        }
                        params_list.append(p_data)
            elif method == 'POST':
                body_data = interface_data.get('body')
                if body_data:
                    mode = body_data['mode']
                    if mode == 'formdata':
                        p_list = body_data['formdata']
                        if p_list:
                            for p in p_list:
                                p_data = {
                                    'param_name': p['key'],
                                    'param_desc': p['description'],
                                    'necessary': True if p.get('disabled') else False,
                                    'default': p['value'],
                                }
                                params_list.append(p_data)
                    elif mode == 'urlencoded':
                        p_list = body_data['urlencoded']
                        if p_list:
                            for p in p_list:
                                p_data = {
                                    'param_name': p['key'],
                                    'param_desc': p['description'],
                                    'necessary': True if p.get('disabled') else False,
                                    'default': p['value'],
                                }
                                params_list.append(p_data)
                    elif mode == 'raw':
                        p_list = body_data['raw']
                        if p_list:
                            p_list = json.loads(p_list)
                            for k, v in p_list.items():
                                p_data = {
                                    'param_name': k,
                                    'param_desc': '',
                                    'necessary': True,
                                    'default': v,
                                }
                                params_list.append(p_data)
            new_data = {
                'interface_name': interface_name,
                'interface_desc': interface_desc,
                'interface_type': interface_type,
                'method': method,
                'path': path,
                'header': header,
                'params': params_list,
                'response': '',
            }
            data_list.append(new_data)
        return data_list
