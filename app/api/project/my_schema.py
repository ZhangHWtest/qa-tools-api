# -*- coding: utf-8 -*-

pro_list_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "project list",
    "description": "project list",
    "type": "object",
    "properties": {
        "project_name": {
            "description": "project name",
            "type": "string",
            "minLength": 0,
            "maxLength": 30
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
    "minProperties": 0,
    "maxProperties": 3,
}

pro_info_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "project info",
    "description": "project info by id",
    "type": "object",
    "properties": {
        "project_id": {
            "description": "project id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "project_id",
    ]
}

add_pro_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "add project",
    "description": "add a project",
    "type": "object",
    "properties": {
        "project_name": {
            "description": "project name",
            "type": "string",
            "minLength": 1,
            "maxLength": 30
        },
        "project_desc": {
            "description": "project description",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
    },
    "minProperties": 1,
    "maxProperties": 2,
    "required": [
        "project_name",
    ]
}

edit_pro_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "edit project",
    "description": "edit a project by id",
    "type": "object",
    "properties": {
        "project_id": {
            "description": "project id",
            "type": "integer",
        },
        "project_name": {
            "description": "project name",
            "type": "string",
            "minLength": 1,
            "maxLength": 30
        },
        "project_desc": {
            "description": "project description",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
    },
    "minProperties": 2,
    "maxProperties": 3,
    "required": [
        "project_id",
        "project_name",
    ]
}

del_pro_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "delete project",
    "description": "delete a project by id",
    "type": "object",
    "properties": {
        "project_id": {
            "description": "project id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "project_id",
    ]
}
