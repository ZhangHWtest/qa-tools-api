# -*- coding: utf-8 -*-

mf_list_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "manufacturer list",
    "description": "manufacturer list",
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

add_mf_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "add manufacturer",
    "description": "add a manufacturer",
    "type": "object",
    "properties": {
        "mf_name": {
            "description": "manufacturer name",
            "type": "string",
            "minLength": 1,
            "maxLength": 30
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "mf_name",
    ]
}

del_mf_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "delete manufacturer",
    "description": "delete a manufacturer by id",
    "type": "object",
    "properties": {
        "mf_id": {
            "description": "manufacturer id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "mf_id",
    ]
}

eq_list_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "equipment list",
    "description": "equipment list",
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

eq_info_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "equipment info",
    "description": "equipment info by id",
    "type": "object",
    "properties": {
        "eq_id": {
            "description": "equipment id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "eq_id",
    ]
}

add_eq_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "add equipment",
    "description": "add a equipment",
    "type": "object",
    "properties": {
        "eq_code": {
            "description": "equipment code",
            "type": "string",
            "minLength": 1,
            "maxLength": 30
        },
        "eq_name": {
            "description": "equipment name",
            "type": "string",
            "minLength": 1,
            "maxLength": 30
        },
        "eq_desc": {
            "description": "equipment description",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "eq_type": {
            "description": "equipment type, 0 other,1 phone,2 pad",
            "type": "integer",
        },
        "eq_sys": {
            "description": "equipment system, 0 other,1 ios，2 android",
            "type": "integer",
        },
        "eq_sys_ver": {
            "description": "equipment system version",
            "type": "string",
            "minLength": 0,
            "maxLength": 10
        },
        "eq_owner": {
            "description": "equipment owner",
            "type": "string",
            "minLength": 0,
            "maxLength": 10
        },
        "have_sim": {
            "description": "equipment have sim card, 0 no,1 yes",
            "type": "integer",
        },
        "mf_id": {
            "description": "equipment manufacturer id",
            "type": "integer",
        },
    },
    "minProperties": 9,
    "maxProperties": 9,
    "required": [
        "eq_code",
        "eq_name",
        "eq_desc",
        "eq_type",
        "eq_sys",
        "eq_sys_ver",
        "eq_owner",
        "have_sim",
        "mf_id",
    ]
}

edit_eq_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "edit equipment",
    "description": "edit a equipment",
    "type": "object",
    "properties": {
        "eq_id": {
            "description": "equipment id",
            "type": "integer",
        },
        "eq_code": {
            "description": "equipment code",
            "type": "string",
            "minLength": 1,
            "maxLength": 30
        },
        "eq_name": {
            "description": "equipment name",
            "type": "string",
            "minLength": 1,
            "maxLength": 30
        },
        "eq_desc": {
            "description": "equipment description",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "eq_type": {
            "description": "equipment type, 0 other,1 phone,2 pad",
            "type": "integer",
        },
        "eq_sys": {
            "description": "equipment system, 0 other,1 ios，2 android",
            "type": "integer",
        },
        "eq_sys_ver": {
            "description": "equipment system version",
            "type": "string",
            "minLength": 0,
            "maxLength": 10
        },
        "eq_owner": {
            "description": "equipment owner",
            "type": "string",
            "minLength": 0,
            "maxLength": 10
        },
        "borrower": {
            "description": "equipment borrower",
            "type": "string",
            "minLength": 0,
            "maxLength": 10
        },
        "have_sim": {
            "description": "equipment have sim card, 0 no,1 yes",
            "type": "integer",
        },
        "mf_id": {
            "description": "equipment manufacturer id",
            "type": "integer",
        },
    },
    "minProperties": 11,
    "maxProperties": 11,
    "required": [
        "eq_id",
        "eq_code",
        "eq_name",
        "eq_desc",
        "eq_type",
        "eq_sys",
        "eq_sys_ver",
        "eq_owner",
        "borrower",
        "have_sim",
        "mf_id",
    ]
}

switch_eq_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "switch equipment",
    "description": "switch a equipment status",
    "type": "object",
    "properties": {
        "eq_id": {
            "description": "equipment id",
            "type": "integer",
        },
        "borrower": {
            "description": "equipment borrower",
            "type": "string",
            "minLength": 0,
            "maxLength": 10
        },
        "eq_status": {
            "description": "equipment status, 0 stop using,1 not lent，2 lend out",
            "type": "integer",
        },
    },
    "minProperties": 3,
    "maxProperties": 3,
    "required": [
        "eq_id",
        "borrower",
        "eq_status",
    ]
}

del_eq_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "delete equipment",
    "description": "delete a equipment by id",
    "type": "object",
    "properties": {
        "eq_id": {
            "description": "equipment id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "eq_id",
    ]
}

eq_log_list_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "equipment log list",
    "description": "equipment log list",
    "type": "object",
    "properties": {
        "eq_id": {
            "description": "equipment id",
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
        "eq_id",
    ]
}
