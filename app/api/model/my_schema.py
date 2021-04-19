# -*- coding: utf-8 -*-

model_list_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "model list",
    "description": "model list by project id",
    "type": "object",
    "properties": {
        "project_id": {
            "description": "project id",
            "type": "integer",
        },
        "page_num": {
            "description": "page number",
            "type": "integer",
        },
        "page_size": {
            "description": "page size",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 3,
    "required": [
        "project_id",
    ]
}

model_info_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "model info",
    "description": "model info by id",
    "type": "object",
    "properties": {
        "model_id": {
            "description": "model id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "model_id",
    ]
}

add_model_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "add model",
    "description": "add a model",
    "type": "object",
    "properties": {
        "project_id": {
            "description": "project id",
            "type": "integer",
        },
        "model_name": {
            "description": "model name",
            "type": "string",
            "minLength": 1,
            "maxLength": 30
        },
        "model_desc": {
            "description": "model description",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
    },
    "minProperties": 2,
    "maxProperties": 3,
    "required": [
        "project_id",
        "model_name",
    ]
}

edit_model_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "edit model",
    "description": "edit a model by id",
    "type": "object",
    "properties": {
        "model_id": {
            "description": "model id",
            "type": "integer",
        },
        "model_name": {
            "description": "model name",
            "type": "string",
            "minLength": 1,
            "maxLength": 30
        },
        "model_desc": {
            "description": "model description",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
    },
    "minProperties": 2,
    "maxProperties": 3,
    "required": [
        "model_id",
        "model_name",
    ]
}

del_model_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "delete model",
    "description": "delete a model by id",
    "type": "object",
    "properties": {
        "model_id": {
            "description": "model id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "model_id",
    ]
}
