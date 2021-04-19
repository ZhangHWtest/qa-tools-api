# -*- coding: utf-8 -*-

user_list_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "user list",
    "description": "user list",
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

add_user_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "add user",
    "description": "add a user",
    "type": "object",
    "properties": {
        "username": {
            "description": "user name",
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
    "minProperties": 2,
    "maxProperties": 2,
    "required": [
        "username",
        "email"
    ]
}

change_pass_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "change password",
    "description": "change current user password",
    "type": "object",
    "properties": {
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
    },
    "minProperties": 2,
    "maxProperties": 2,
    "required": [
        "password",
        "set_password",
    ]
}

reset_pass_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "reset password",
    "description": "reset user password by uid",
    "type": "object",
    "properties": {
        "uid": {
            "description": "user id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "uid",
    ]
}

onoff_user_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "onoff password",
    "description": "switch on/off user status",
    "type": "object",
    "properties": {
        "uid": {
            "description": "user id",
            "type": "integer",
        },
        "status": {
            "description": "user status 0/1",
            "type": "integer",
        },
    },
    "minProperties": 2,
    "maxProperties": 2,
    "required": [
        "uid",
        "status",
    ]
}

set_role_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "set role",
    "description": "set user role by uid",
    "type": "object",
    "properties": {
        "uid": {
            "description": "user id",
            "type": "integer",
        },
        "role_id": {
            "description": "user role id",
            "type": "integer",
        },
    },
    "minProperties": 2,
    "maxProperties": 2,
    "required": [
        "uid",
        "role_id",
    ]
}
