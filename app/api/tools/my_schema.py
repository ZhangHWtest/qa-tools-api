# -*- coding: utf-8 -*-

LiveLessonToday_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "live lesson today",
    "description": "today‘s live lesson info",
    "type": "object",
    "properties": {
        "pageSize": {
            "description": "page size",
            "type": "integer",
        },
        "pageNum": {
            "description": "page number",
            "type": "integer",
        },
    },
    "minProperties": 2,
    "maxProperties": 2,
    "required": [
        "pageSize",
        "pageNum",
    ]
}

LiveLessonYesterday_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "live lesson yesterday",
    "description": "yesterday‘s live lesson info",
    "type": "object",
    "properties": {
        "pageSize": {
            "description": "page size",
            "type": "integer",
        },
        "pageNum": {
            "description": "page number",
            "type": "integer",
        },
    },
    "minProperties": 2,
    "maxProperties": 2,
    "required": [
        "pageSize",
        "pageNum",
    ]
}

CourseInfoByMobile_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "course info by mobile",
    "description": "course info by mobile",
    "type": "object",
    "properties": {
        "mobile": {
            "description": "user mobile",
            "type": "integer",
        },
        "pageSize": {
            "description": "page size",
            "type": "integer",
        },
        "pageNum": {
            "description": "page number",
            "type": "integer",
        },
    },
    "minProperties": 3,
    "maxProperties": 3,
    "required": [
        "mobile",
        "pageSize",
        "pageNum",
    ]
}

AuthRecordByMobile_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "auth record by mobile",
    "description": "auth record by mobile",
    "type": "object",
    "properties": {
        "mobile": {
            "description": "user mobile",
            "type": "integer",
        },
        "pageSize": {
            "description": "page size",
            "type": "integer",
        },
        "pageNum": {
            "description": "page number",
            "type": "integer",
        },
    },
    "minProperties": 3,
    "maxProperties": 3,
    "required": [
        "mobile",
        "pageSize",
        "pageNum",
    ]
}

UserInfoByXid_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "user info by xid",
    "description": "user info by xid",
    "type": "object",
    "properties": {
        "xid": {
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 5,
            },
            "minItems": 1,
            "maxItems": 10,
            "uniqueItems": True
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "xid",
    ]
}

CourseInfoByLiveId_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "course info by live_id",
    "description": "course info by live_id",
    "type": "object",
    "properties": {
        "live_id": {
            "description": "hky live id",
            "type": "string",
            "minLength": 1,
            "maxLength": 30
        },
    },
    "minProperties": 1,
    "maxProperties": 1,
    "required": [
        "live_id",
    ]
}
