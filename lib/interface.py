#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import Flask, request, abort
from flask_cors import CORS
from lib.pager import Pager
from lib.live_lesson_info import get_live_lesson_today, get_live_lesson_yesterday

server = Flask(__name__)
CORS(server, resources=r'/*')


@server.route('/today_lesson', methods=['GET', 'POST'])
def live_lesson_today():
    if request.method == 'POST':
        page_size = request.json.get('pageSize')
        page_num = request.json.get('pageNum')
        data = get_live_lesson_today()
        pager = Pager(data, page_size)
        data = pager.page_data(page_num)
        res = {
            'msg': 'success',
            'code': 1,
            'data': data,
            'page_size': pager.page_size,   # 每页最大值
            'page_num': page_num,           # 当前页数
            'page_total': pager.page_num    # 最大页数
        }
        return json.dumps(res, ensure_ascii=False)
    else:
        abort(405)


@server.route('/yesterday_lesson', methods=['GET', 'POST'])
def live_lesson_yesterday():
    if request.method == 'POST':
        page_size = request.json.get('pageSize')
        page_num = request.json.get('pageNum')
        data = get_live_lesson_yesterday()
        pager = Pager(data, page_size)
        data = pager.page_data(page_num)
        res = {
            'msg': 'success',
            'code': 1,
            'data': data,
            'page_size': pager.page_size,
            'page_num': page_num,
            'page_total': pager.page_num
        }
        return json.dumps(res, ensure_ascii=False)
    else:
        abort(405)


@server.route('/test_pager', methods=['GET', 'POST'])
def test_pager():
    if request.method == 'POST':
        page_size = request.json.get('pageSize')
        page_num = request.json.get('pageNum')
        data = get_live_lesson_yesterday()
        pager = Pager(data, page_size)
        data = pager.page_data(page_num)
        res = {
            'msg': 'success',
            'code': 1,
            'data': data,
            'page_size': pager.page_size,
            'page_num': page_num,
            'page_total': pager.page_num
        }
        return json.dumps(res, ensure_ascii=False)
    else:
        abort(405)


