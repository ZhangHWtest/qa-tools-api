# -*- coding: utf-8 -*-
"""
判断
"""
from common.fengzhuang_dict import getdictvalue
from common.get_value import get_value_from_dict


def assert_in(asserqiwang, fanhuijson):
    if len(asserqiwang.split('=')) > 1:
        data = asserqiwang.split('&')
        res = dict([(item.split('=')) for item in data])
        try:
            value1 = [(str(getdictvalue(fanhuijson,key)[0])) for key in res.keys()]
            value2 = [(str(value)) for value in res.values()]
            if value1 == value2:
                return 'pass'
            else:
                return 'fail'
        except:
            return 'exception '
    else:
        return '请检查断言'


def assert_contain(res_assert, res_dict):
    """检查返回结果是否包含期望key-value"""
    different_data = dict()
    for key, value1 in res_assert.items():
        value2 = get_value_from_dict(res_dict, key)
        if value1 != value2:
            different_data[key] = value2
    return different_data


def assertre(asserqingwang):
    if len(asserqingwang.split('=')) > 1:
        data = asserqingwang.split('&')
        result = dict([(item.split('=')) for item in data])
        return result
    else:
        return u'请填写期望值'


def pare_result_mysql(mysqlresult, paseziduan, return_result):
    mysql_list = []
    for i in mysqlresult:
        mysql_list.append(i)
    test_result = []
    ziduanlist = []
    if paseziduan is None:
        return {'code': 0, 'result': 'pass'}
    try:
        for ziduan in paseziduan:
            ziduanlist.append(ziduan[0].split(','))
    except Exception as e:
        return {'code': 1, 'result': e}
    try:
        for ziduan in ziduanlist:
            test_result.append(return_result[ziduan])
    except Exception as e:
        return {'code': 1, 'result': e}
    if test_result == mysql_list:
        return {'code': 2, 'result': 'pass'}
    else:
        return {'code': 3, 'result': 'fail'}


def compare_two_dict(src_data, dst_data):
    try:
        assert type(src_data) == type(dst_data)
    except AssertionError:
        return {'code': -1, 'result': 'fail', 'msg': '返回数据与预期结果数据类型不一致'}
    if isinstance(src_data, dict):
        for key in src_data:
            try:
                assert key in dst_data
            except AssertionError:
                return {'code': -1, 'result': 'fail', 'msg': '预期结果的 %s 不在返回数据中' % key}
            compare_two_dict(src_data[key], dst_data[key])
    elif isinstance(src_data, (list, tuple)):
        try:
            assert len(src_data) == len(dst_data)
        except AssertionError:
            return {'code': -1, 'result': 'fail', 'msg': '返回数据与预期结果数据长度不一致'}

        for src_list, dst_list in zip(sorted(src_data), sorted(dst_data)):
            compare_two_dict(src_list, dst_list)
    else:
        try:
            assert src_data == dst_data
            return {'code': 1, 'result': 'pass', 'msg': '返回数据与预期结果一致'}
        except AssertionError:
            return {'code': -1, 'result': 'fail', 'msg': '返回数据与预期结果数据值不一致'}


def dict_diff_data(first, second):
    """
    get the different data bewtten two dicts objects
    return :result = first - second
    """
    assert isinstance(first, dict)
    assert isinstance(second, dict)
    different_data = {}
    update_key = set(first).intersection(set(second))
    insert_key = set(first).difference(set(second))
    delete_key = set(second).difference(set(first))
    # updata data item which are both on first and second  and Not equal values
    for k in update_key:
        if isinstance(first[k], dict):
            res = dict_diff_data(first[k], second[k])
            if len(res) > 0:
                different_data[k] = res
        elif first[k] != second[k]:
            different_data[k] = first[k]
    # insert new item from first
    for k in insert_key:
        different_data[k] = first[k]
    # delete data
    for k in delete_key:
        different_data[k] = None
    return different_data


if __name__ == "__main__":
    dic1 = {
        'name': 'test',
        'score': 89
    }
    dic2 = {
        'name': 'test',
        'score': 29,
        'age': 23
    }
    result = dict_diff_data(dic2, dic1)
    print(result)
