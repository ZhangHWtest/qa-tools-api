# -*- coding: utf-8 -*-

mock_list_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "mock list",
    "description": "mock list",
    "type": "object",
    "properties": {
        "page_num": {
            "description": "page number",
            "type": "integer",
        },
        "page_size": {
            "description": "page size",
            "type": "integer",
        },
    },
    "minProperties": 0,
    "maxProperties": 2,
}

mock_info_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "mock info",
    "description": "mock info by id",
    "type": "object",
    "properties": {
        "mock_id": {
            "description": "mock id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "mock_id",
    ]
}

add_mock_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "add mock",
    "description": "add a mock",
    "type": "object",
    "properties": {
        "mock_name": {
            "description": "mock name",
            "type": "string",
            "minLength": 1,
            "maxLength": 60
        },
        "mock_desc": {
            "description": "mock description",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "method": {
            "description": "mock request method",
            "type": "string",
            "minLength": 1,
            "maxLength": 10
        },
        "path": {
            "description": "mock request path",
            "type": "string",
            "minLength": 1,
            "maxLength": 100
        },
        "params": {
            "description": "mock request params",
            "type": "string",
            "minLength": 0,
            "maxLength": 1000
        },
        "header": {
            "description": "mock request header",
            "type": "string",
            "minLength": 0,
            "maxLength": 1000
        },
        "response": {
            "description": "mock response",
            "type": "string",
            "minLength": 1,
            "maxLength": 1000
        },
        "res_type": {
            "description": "mock response type",
            "type": "string",
            "minLength": 1,
            "maxLength": 10
        },
        "check_params": {
            "description": "whether check mock params 0/1",
            "type": "integer",
        },
        "check_header": {
            "description": "whether check mock header 0/1",
            "type": "integer",
        },
    },
    "minProperties": 7,
    "maxProperties": 10,
    "required": [
        "mock_name",
        "method",
        "path",
        "response",
        "res_type",
        "check_params",
        "check_header",
    ]
}

edit_mock_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "edit mock",
    "description": "edit a mock by id",
    "type": "object",
    "properties": {
        "mock_id": {
            "description": "mock id",
            "type": "integer",
        },
        "mock_name": {
            "description": "mock name",
            "type": "string",
            "minLength": 1,
            "maxLength": 60
        },
        "mock_desc": {
            "description": "mock description",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "method": {
            "description": "mock request method",
            "type": "string",
            "minLength": 1,
            "maxLength": 10
        },
        "path": {
            "description": "mock request path",
            "type": "string",
            "minLength": 1,
            "maxLength": 100
        },
        "params": {
            "description": "mock request params",
            "type": "string",
            "minLength": 0,
            "maxLength": 1000
        },
        "header": {
            "description": "mock request header",
            "type": "string",
            "minLength": 0,
            "maxLength": 1000
        },
        "response": {
            "description": "mock response",
            "type": "string",
            "minLength": 1,
            "maxLength": 1000
        },
        "res_type": {
            "description": "mock response type",
            "type": "string",
            "minLength": 1,
            "maxLength": 10
        },
        "check_params": {
            "description": "whether check mock params 0/1",
            "type": "integer",
        },
        "check_header": {
            "description": "whether check mock header 0/1",
            "type": "integer",
        },
    },
    "minProperties": 8,
    "maxProperties": 11,
    "required": [
        "mock_id",
        "mock_name",
        "method",
        "path",
        "response",
        "res_type",
        "check_params",
        "check_header",
    ]
}

del_mock_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "delete mock",
    "description": "delete a mock by id",
    "type": "object",
    "properties": {
        "mock_id": {
            "description": "mock id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "mock_id",
    ]
}
