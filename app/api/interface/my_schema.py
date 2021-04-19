# -*- coding: utf-8 -*-

interface_list_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "interface list",
    "description": "interface list",
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
        "interface_name": {
            "description": "interface name keyword",
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
    "maxProperties": 5,
}

interface_info_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "interface info",
    "description": "interface info by id",
    "type": "object",
    "properties": {
        "interface_id": {
            "description": "interface id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "interface_id",
    ]
}

add_interface_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "add interface",
    "description": "add a interface",
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
        "interface_name": {
            "description": "interface name",
            "type": "string",
            "minLength": 1,
            "maxLength": 30
        },
        "interface_desc": {
            "description": "interface description",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "interface_type": {
            "description": "interface request type, http/https",
            "type": "string",
            "minLength": 1,
            "maxLength": 10
        },
        "method": {
            "description": "interface request method, GET/POST",
            "type": "string",
            "minLength": 1,
            "maxLength": 10
        },
        "path": {
            "description": "interface request path",
            "type": "string",
            "minLength": 2,
            "maxLength": 100
        },
    },
    "minProperties": 4,
    "maxProperties": 7,
    "required": [
        "project_id",
        "interface_name",
        "method",
        "path",
    ]
}

edit_interface_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "edit interface",
    "description": "edit a interface by id",
    "type": "object",
    "properties": {
        "interface_id": {
            "description": "interface id",
            "type": "integer",
        },
        "interface_name": {
            "description": "interface name",
            "type": "string",
            "minLength": 1,
            "maxLength": 30
        },
        "interface_desc": {
            "description": "interface description",
            "type": "string",
            "minLength": 0,
            "maxLength": 60
        },
        "interface_type": {
            "description": "interface request type, http/https",
            "type": "string",
            "minLength": 1,
            "maxLength": 10
        },
        "method": {
            "description": "interface request method, GET/POST",
            "type": "string",
            "minLength": 1,
            "maxLength": 10
        },
        "path": {
            "description": "interface request path",
            "type": "string",
            "minLength": 2,
            "maxLength": 100
        },
    },
    "minProperties": 4,
    "maxProperties": 6,
    "required": [
        "interface_id",
        "interface_name",
        "method",
        "path",
    ]
}

move_interface_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "move interface",
    "description": "move a interface to a model or a project",
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
    },
    "minProperties": 2,
    "maxProperties": 3,
    "required": [
        "project_id",
        "interface_id",
    ]
}

del_interface_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "delete interface",
    "description": "delete a interface by id",
    "type": "object",
    "properties": {
        "interface_id": {
            "description": "interface id",
            "type": "integer",
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "interface_id",
    ]
}

edd_param_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "add parameter",
    "description": "add a parameter",
    "type": "object",
    "properties": {
        "interface_id": {
            "description": "interface id",
            "type": "integer",
        },
        "params": {
            "type": "array",
            "items": [
                {
                    "type": "object",
                    "properties": {
                        "param_name": {
                            "description": "parameter name",
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 30
                        },
                        "param_desc": {
                            "description": "parameter description",
                            "type": "string",
                            "minLength": 0,
                            "maxLength": 200
                        },
                        "is_necessary": {
                            "description": "parameter whether necessary",
                            "type": "integer",
                        },
                        "default": {
                            "description": "parameter default value",
                            "type": "string",
                            "minLength": 0,
                            "maxLength": 60
                        },
                    },
                },
            ],
            "minItems": 0,
        },
        # "param_name": {
        #     "description": "parameter name",
        #     "type": "string",
        #     "minLength": 1,
        #     "maxLength": 30
        # },
        # "param_desc": {
        #     "description": "parameter description",
        #     "type": "string",
        #     "minLength": 0,
        #     "maxLength": 60
        # },
        # "is_necessary": {
        #     "description": "parameter whether necessary",
        #     "type": "integer",
        # },
        # "default": {
        #     "description": "parameter default value",
        #     "type": "string",
        #     "minLength": 0,
        #     "maxLength": 30
        # },
    },
    "minProperties": 2,
    "maxProperties": 2,
    "required": [
        "interface_id",
        "params",
    ]
}

edit_header_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "edit header",
    "description": "edit a header by interface id",
    "type": "object",
    "properties": {
        "interface_id": {
            "description": "interface id",
            "type": "integer",
        },
        "header": {
            "description": "interface header",
            "type": "string",
            "minLength": 0,
            "maxLength": 200,
        },
    },
    "minProperties": 0,
    "maxProperties": 2,
}

edit_response_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "edit response",
    "description": "edit a response by interface id",
    "type": "object",
    "properties": {
        "interface_id": {
            "description": "interface id",
            "type": "integer",
        },
        "response": {
            "description": "interface response",
            "type": "string",
            "minLength": 0,
            "maxLength": 200,
        },
    },
    "minProperties": 0,
    "maxProperties": 2,
}

import_json_data_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "import json data interface",
    "description": "import json data interface",
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
        "file_name": {
            "description": "upload file name",
            "type": "string",
            "minLength": 1,
            "maxLength": 30
        },
        "json_type": {
            "description": "json file type, yapi/postman",
            "type": "string",
            "minLength": 1,
            "maxLength": 10
        },
    },
    "minProperties": 3,
    "maxProperties": 4,
    "required": [
        "project_id",
        "file_name",
        "json_type",
    ]
}
