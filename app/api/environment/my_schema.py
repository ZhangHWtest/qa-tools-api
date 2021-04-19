# -*- coding: utf-8 -*-

env_list_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "environment list",
    "description": "environment list",
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

env_info_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "environment info",
    "description": "environment info by id",
    "type": "object",
    "properties": {
        "env_id": {
            "description": "environment id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "env_id",
    ]
}

add_env_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "add environment",
    "description": "add a environment",
    "type": "object",
    "properties": {
        "env_name": {
            "description": "environment name",
            "type": "string",
            "minLength": 1,
            "maxLength": 30
        },
        "desc": {
            "description": "environment description",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "url": {
            "description": "environment domain name",
            "type": "string",
            "minLength": 10,
            "maxLength": 60
        },
        "use_db": {
            "description": "environment whether to use database",
            "type": "integer",
        },
        "db_host": {
            "description": "database host",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "db_port": {
            "description": "database port",
            "type": "string",
            "minLength": 0,
            "maxLength": 10
        },
        "db_user": {
            "description": "database login user name",
            "type": "string",
            "minLength": 0,
            "maxLength": 30
        },
        "db_pass": {
            "description": "database login password",
            "type": "string",
            "minLength": 0,
            "maxLength": 30
        },
        "database": {
            "description": "database name",
            "type": "string",
            "minLength": 0,
            "maxLength": 30
        },
    },
    "minProperties": 3,
    "maxProperties": 9,
    "required": [
        "env_name",
        "url",
        "use_db",
    ]
}

edit_env_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "edit environment",
    "description": "edit a environment",
    "type": "object",
    "properties": {
        "env_id": {
            "description": "environment id",
            "type": "integer",
        },
        "env_name": {
            "description": "environment name",
            "type": "string",
            "minLength": 1,
            "maxLength": 30
        },
        "desc": {
            "description": "environment description",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "url": {
            "description": "environment domain name",
            "type": "string",
            "minLength": 10,
            "maxLength": 60
        },
        "use_db": {
            "description": "environment whether to use database",
            "type": "integer",
        },
        "db_host": {
            "description": "database host",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "db_port": {
            "description": "database port",
            "type": "string",
            "minLength": 0,
            "maxLength": 10
        },
        "db_user": {
            "description": "database login user name",
            "type": "string",
            "minLength": 0,
            "maxLength": 30
        },
        "db_pass": {
            "description": "database login password",
            "type": "string",
            "minLength": 0,
            "maxLength": 30
        },
        "database": {
            "description": "database name",
            "type": "string",
            "minLength": 0,
            "maxLength": 30
        },
    },
    "minProperties": 4,
    "maxProperties": 10,
    "required": [
        "env_id",
        "env_name",
        "url",
        "use_db",
    ]
}

del_env_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "delete environment",
    "description": "delete a environment by id",
    "type": "object",
    "properties": {
        "env_id": {
            "description": "environment id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "env_id",
    ]
}
