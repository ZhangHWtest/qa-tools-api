# -*- coding: utf-8 -*-

case_list_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "case list",
    "description": "case list",
    "type": "object",
    "properties": {
        "project_id": {
            "description": "project id",
            "type": "integer",
        },
        "model_id": {
            "description": "model id",
            "type": "integer",
        },
        "interface_id": {
            "description": "interface id",
            "type": "integer",
        },
        "case_name": {
            "description": "case name keyword",
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
    "maxProperties": 6,
}

case_info_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "case info",
    "description": "case info by id",
    "type": "object",
    "properties": {
        "case_id": {
            "description": "case id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "case_id",
    ]
}

add_case_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "add case",
    "description": "add a case",
    "type": "object",
    "properties": {
        "interface_id": {
            "description": "interface id",
            "type": "integer",
        },
        "env_id": {
            "description": "environment id",
            "type": "integer",
        },
        "case_name": {
            "description": "case name",
            "type": "string",
            "minLength": 1,
            "maxLength": 30
        },
        "case_desc": {
            "description": "case description",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "case_type": {
            "description": "case request type, http/https",
            "type": "string",
            "minLength": 1,
            "maxLength": 10
        },
        "method": {
            "description": "case request method, GET/POST",
            "type": "string",
            "minLength": 1,
            "maxLength": 10
        },
        "path": {
            "description": "case request path",
            "type": "string",
            "minLength": 2,
            "maxLength": 100
        },
        "params": {
            "description": "case request with parameters",
            "type": "string",
            "minLength": 0,
            "maxLength": 1000
        },
        "header": {
            "description": "case request with header",
            "type": "string",
            "minLength": 0,
            "maxLength": 1000
        },
        "has_sign": {
            "description": "whether case need sign 0/1",
            "type": "integer",
        },
        "ak": {
            "description": "app id",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "sk": {
            "description": "app secret key",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "res_assert": {
            "description": "assert case response",
            "type": "string",
            "minLength": 1,
            "maxLength": 200
        },
        "has_rely": {
            "description": "whether case has rely 0/1",
            "type": "integer",
        },
        "rely_info": {
            "description": "rely case info",
            "type": "string",
            "minLength": 0,
            "maxLength": 200
        },
        "has_output": {
            "description": "whether case save result 0/1",
            "type": "integer",
        },
        "output_para": {
            "description": "case output param",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "has_input": {
            "description": "whether case save result 0/1",
            "type": "integer",
        },

        "input_para": {
            "description": "case input param",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "input_header": {
            "description": "case input header",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "save_result": {
            "description": "whether case save result 0/1",
            "type": "integer",
        },
        "use_db": {
            "description": "whether case use database 0/1",
            "type": "integer",
        },
        "sql": {
            "description": "sql",
            "type": "string",
            "minLength": 0,
            "maxLength": 1000
        },
        "field_value": {
            "description": "database field value",
            "type": "string",
            "minLength": 0,
            "maxLength": 100
        },
    },
    "minProperties": 12,
    "maxProperties": 24,
    "required": [
        "interface_id",
        "env_id",
        "case_name",
        "method",
        "path",
        "has_sign",
        "res_assert",
        "has_rely",
        "has_output",
        "has_input",
        "save_result",
        "use_db",
    ]
}

edit_case_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "edit case",
    "description": "edit a case",
    "type": "object",
    "properties": {
        "case_id": {
            "description": "case id",
            "type": "integer",
        },
        "env_id": {
            "description": "environment id",
            "type": "integer",
        },
        "case_name": {
            "description": "case name",
            "type": "string",
            "minLength": 1,
            "maxLength": 30
        },
        "case_desc": {
            "description": "case description",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "case_type": {
            "description": "case request type, http/https",
            "type": "string",
            "minLength": 1,
            "maxLength": 10
        },
        "method": {
            "description": "case request method, GET/POST",
            "type": "string",
            "minLength": 1,
            "maxLength": 10
        },
        "path": {
            "description": "case request path",
            "type": "string",
            "minLength": 2,
            "maxLength": 100
        },
        "params": {
            "description": "case request with parameters",
            "type": "string",
            "minLength": 0,
            "maxLength": 1000
        },
        "header": {
            "description": "case request with header",
            "type": "string",
            "minLength": 0,
            "maxLength": 1000
        },
        "has_sign": {
            "description": "whether case need sign 0/1",
            "type": "integer",
        },
        "ak": {
            "description": "app id",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "sk": {
            "description": "app secret key",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "res_assert": {
            "description": "assert case response",
            "type": "string",
            "minLength": 1,
            "maxLength": 200
        },
        "has_rely": {
            "description": "whether case has rely 0/1",
            "type": "integer",
        },
        "rely_info": {
            "description": "rely case info",
            "type": "string",
            "minLength": 0,
            "maxLength": 200
        },
        "has_output": {
            "description": "whether case save result 0/1",
            "type": "integer",
        },
        "output_para": {
            "description": "case output param",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "has_input": {
            "description": "whether case save result 0/1",
            "type": "integer",
        },

        "input_para": {
            "description": "case input param",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "input_header": {
            "description": "case input header",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "save_result": {
            "description": "whether case save result 0/1",
            "type": "integer",
        },
        "use_db": {
            "description": "whether case use database 0/1",
            "type": "integer",
        },
        "sql": {
            "description": "sql",
            "type": "string",
            "minLength": 0,
            "maxLength": 1000
        },
        "field_value": {
            "description": "database field value",
            "type": "string",
            "minLength": 0,
            "maxLength": 100
        },
    },
    "minProperties": 12,
    "maxProperties": 24,
    "required": [
        "case_id",
        "env_id",
        "case_name",
        "method",
        "path",
        "has_sign",
        "res_assert",
        "has_rely",
        "has_output",
        "has_input",
        "save_result",
        "use_db",
    ]
}

duplicate_case_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "duplicate case",
    "description": "duplicate a case by id",
    "type": "object",
    "properties": {
        "case_id": {
            "description": "case id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "case_id",
    ]
}

del_case_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "delete case",
    "description": "delete a case by id",
    "type": "object",
    "properties": {
        "case_id": {
            "description": "case id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "case_id",
    ]
}

run_single_case_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "run single case",
    "description": "run single case by id",
    "type": "object",
    "properties": {
        "case_id": {
            "description": "case id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "case_id",
    ]
}

run_multiple_case_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "run cases",
    "description": "run cases by id list",
    "type": "object",
    "properties": {
        "project_id": {
            "description": "project id",
            "type": "integer",
        },
        "case_list": {
            "type": "array",
            "items": {
                "type": "integer"
            },
            "minItems": 1,
            "maxItems": 10,
        },

    },
    "minProperties": 1,
    "maxProperties": 2,
    "required": [
        "case_list",
    ]
}

case_res_list_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "case result list",
    "description": "case result list",
    "type": "object",
    "properties": {
        "case_id": {
            "description": "case id",
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
        "case_id",
    ]
}

case_res_info_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "case result info",
    "description": "case result info by id",
    "type": "object",
    "properties": {
        "case_result_id": {
            "description": "case result id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "case_result_id",
    ]
}
