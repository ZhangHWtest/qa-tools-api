# -*- coding: utf-8 -*-


def get_value_from_dict(dic, key, default=None):
    """返回第一个遍历到的key-value，否则返回None"""
    try:
        for k, v in dic.items():
            if k == key:
                return v
            else:
                if isinstance(v, dict):
                    ret = get_value_from_dict(v, key, default)
                    if ret is not default:
                        return ret
                elif isinstance(v, (list, tuple)):
                    for i in range(len(v)):
                        ret = get_value_from_dict(v[i], key, default)
                        if ret is not default:
                            return ret
        return default
    except:
        return default


def get_data_from_postman_json(json_dic, key, result_list):
    """递归获取Postman接口json数据文件中key='item'的值，返回所有值的List"""
    if key in json_dic.keys():
        for value in json_dic[key]:
            if key in value.keys():
                result_list = get_data_from_postman_json(value, key, result_list)
            else:
                result_list.append(value)
    return result_list


def mma_list(listx):
    """返回list列表中大于0的数字的最大值、最小值和平均值"""
    my_list = list()
    for m in listx:
        if m >= 0:
            my_list.append(m)
    if len(my_list) > 0:
        num = 0
        for n in my_list:
            num = num + n
        avg = num / len(my_list)
    else:
        avg = 0
    return max(my_list), min(my_list), avg


if __name__ == '__main__':
    dic = {
        'a': 1,
        'b': 2,
        'c': {
            'd': 4,
            'dd': [{'e': 5, 'f': 6}, {'g': 7}],
            'ddd': ({'h': 8}, {'i': 9, 'j': 10})
        }
    }
    v = get_value_from_dict(dic, 'j')
    print(v)
    print(dic.keys())
