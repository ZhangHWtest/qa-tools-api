# -*- coding: utf-8 -*-

task_list_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "case list",
    "description": "case list",
    "type": "object",
    "properties": {
        "project_id": {
            "description": "project id",
            "type": "integer",
        },
        "task_name": {
            "description": "task name keyword",
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
    "maxProperties": 4,
}

task_info_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "task info",
    "description": "task info by id",
    "type": "object",
    "properties": {
        "task_id": {
            "description": "task id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "task_id",
    ]
}

add_task_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "add task",
    "description": "add a task",
    "type": "object",
    "properties": {
        "project_id": {
            "description": "project id",
            "type": "integer",
        },
        "task_name": {
            "description": "task name",
            "type": "string",
            "minLength": 1,
            "maxLength": 30
        },
        "task_type": {
            "description": "task type, 0/1/2/3",
            "type": "integer",
        },
        "run_time": {
            "description": "task run time setting",
            "type": "string",
            "minLength": 0,
            "maxLength": 30
        },
    },
    "minProperties": 3,
    "maxProperties": 4,
    "required": [
        "task_name",
        "task_type",
        "run_time",
    ]
}

edit_task_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "edit task",
    "description": "edit a task",
    "type": "object",
    "properties": {
        "project_id": {
            "description": "project id",
            "type": "integer",
        },
        "task_id": {
            "description": "task id",
            "type": "integer",
        },
        "task_name": {
            "description": "task name",
            "type": "string",
            "minLength": 1,
            "maxLength": 30
        },
        "task_type": {
            "description": "task type, 0/1/2/3",
            "type": "integer",
        },
        "run_time": {
            "description": "task run time setting",
            "type": "string",
            "minLength": 0,
            "maxLength": 30
        },
    },
    "minProperties": 4,
    "maxProperties": 5,
    "required": [
        "task_id",
        "task_name",
        "task_type",
        "run_time",
    ]
}

update_case_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "update case",
    "description": "update case in the task",
    "type": "object",
    "properties": {
        "task_id": {
            "description": "task id",
            "type": "integer",
        },
        "case_list": {
            "type": "array",
            "items": {
                "type": "integer"
            },
            "minItems": 0,
            "maxItems": 10,
        },
    },
    "minProperties": 2,
    "maxProperties": 2,
    "required": [
        "task_id",
        "case_list",
    ]
}


task_res_list_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "task result list",
    "description": "task result list",
    "type": "object",
    "properties": {
        "task_id": {
            "description": "task id",
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
        "task_id",
    ]
}

task_res_info_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "task result info",
    "description": "task result info by id",
    "type": "object",
    "properties": {
        "task_result_id": {
            "description": "task result id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "task_result_id",
    ]
}
