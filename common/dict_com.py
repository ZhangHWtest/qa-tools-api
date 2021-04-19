# -*- coding: utf-8 -*-


def comp_dict(dict1, dict2):
    """字典比较判断"""
    try:
        for k, v in dict1.items():
            for k2, v2 in dict2.items():
                if k == k2 and v == v2:
                    return True
                else:
                    return False
    except:
        return False


def assert_in(asserqiwang, fanhuijson):
    """断言封装,断言切割根据&切割"""
    if len(asserqiwang.split('=')) > 1:
        try:
            data = asserqiwang.split('&')
            result = dict([(item.split('=')) for item in data])
            value1 = ([(str(fanhuijson[key])) for key in result.keys()])
            value2 = ([(str(value)) for value in result.values()])
            if value1 == value2:
                return 'pass'
            else:
                return 'fail'
        except Exception as e:
            return '异常！原因：%s' % e
    else:
        return '预期不存在'


def dict_par(dict1, dict2):
    x = []
    y = []
    try:
        for k, v in dict1.items():
            x.append(k)
        for k2, v2 in dict2.items():
            y.append(k2)
    except:
        return False
    if x == y:
        return True
    else:
        return False

