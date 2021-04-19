# -*- coding: utf-8 -*-

import json
from jsonschema import validate, draft7_format_checker
from jsonschema.exceptions import SchemaError, ValidationError


def format_checker(schema, json_data):
    try:
        validate(instance=json_data, schema=schema, format_checker=draft7_format_checker)
    except SchemaError as e:
        mes = "验证模式错误，位置为{}，信息为{}".format(" --> ".join([i for i in e.path]), e.message)
        return False, mes
    except ValidationError as e:
        mes = "参数不符合规定，出错字段为{}，提示信息为{}".format(" --> ".join([str(i) for i in e.path]), e.message)
        return False, mes
    else:
        return True, ''


def is_json(mes):
    try:
        json.loads(mes)
    except:
        return False
    return True
