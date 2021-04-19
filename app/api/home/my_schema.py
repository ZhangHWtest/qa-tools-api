# -*- coding: utf-8 -*-

login_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "login info",
    "description": "user login info",
    "type": "object",
    "properties": {
        "username": {
            "description": "user name",
            "type": "string",
            "minLength": 2,
            "maxLength": 30
        },
        "password": {
            "description": "user password",
            "type": "string",
            "minLength": 2,
            "maxLength": 30
        },
    },
    "minProperties": 2,
    "maxProperties": 2,
    "required": [
        "username",
        "password"
    ]
}

reg_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "register info",
    "description": "user register info",
    "type": "object",
    "properties": {
        "username": {
            "description": "user name",
            "type": "string",
            "minLength": 2,
            "maxLength": 30
        },
        "password": {
            "description": "user password",
            "type": "string",
            "minLength": 2,
            "maxLength": 30
        },
        "set_password": {
            "description": "user set password",
            "type": "string",
            "minLength": 2,
            "maxLength": 30
        },
        "email": {
            "description": "user email",
            "type": "string",
            "minLength": 5,
            "maxLength": 40
        },
    },
    "minProperties": 4,
    "maxProperties": 4,
    "required": [
        "username",
        "password",
        "set_password",
        "email",
    ]
}

statistics_task_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "statistics task",
    "description": "start statistics task",
    "type": "object",
    "properties": {
        "password": {
            "description": "need password",
            "type": "string",
            "minLength": 2,
            "maxLength": 30
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "password"
    ]
}
test_statistics_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "test statistics",
    "description": "test statistics",
    "type": "object",
    "properties": {
        "password": {
            "description": "need password",
            "type": "string",
            "minLength": 2,
            "maxLength": 30
        },
        "day": {
            "description": "whether case need sign 0/1",
            "type": "integer",
        },
        "save": {
            "description": "whether case need sign 0/1",
            "type": "integer",
        },
    },
    "minProperties": 3,
    "maxProperties": 3,
    "required": [
        "password",
        "day",
        "save",
    ]
}
