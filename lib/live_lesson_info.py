#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 统计CClive直播课信息和数据

from configs import constants
from lib.mydb import MyDB
from lib.local_cache import func_cache
import time
import datetime


@func_cache(expire=300)
def get_live_lesson_today():
    day1 = datetime.date.today()
    day2 = datetime.date.today() + datetime.timedelta(1)
    time1 = int(time.mktime(time.strptime(str(day1), "%Y-%m-%d")))
    time2 = int(time.mktime(time.strptime(str(day2), "%Y-%m-%d")))
    edu_config = constants.MYSQL_EDU
    mysql_edu = MyDB(edu_config)
    sql = "select course_id,content_id,teacher_uid,start_time,callback_key \
            from live_lesson \
            where `start_time` between '%d' and '%d' and live_vendor = 1 \
            order by start_time" % (time1, time2)
    result = mysql_edu.execQuery(sql)
    x = 5
    lesson_list = [result[i:i + x] for i in range(0, len(result), x)]
    data = list()
    for lesson in lesson_list:
        course_id, content_id, teacher_uid, start_time, callback_key = lesson
        sql = "select course_name,school_name \
                from course co inner join school sc on co.school_id = sc.school_id \
                where `course_id` = '%d'" % course_id
        course_name, school_name = mysql_edu.execQuery(sql)
        sql = "select uid from course_auth_record where `course_id` = '%d'" % course_id
        list1 = mysql_edu.execQuery(sql)
        sql = "select student_uid from course_student where `course_id` = '%d'" % course_id
        list2 = mysql_edu.execQuery(sql)
        list3 = [x for x in list1 if x in list2]
        student_number = len(list1 + list2) - len(list3)
        sql = "select content_title from content where `content_id` = '%d'" % content_id
        content_title = mysql_edu.execQuery(sql)[0]
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
        sql = "select nickname,realname,mobile from manager where `uid` = '%d'" % teacher_uid
        nickname, realname, mobile = mysql_edu.execQuery(sql)
        teacher_info = "%d/%s/%s/%s" % (teacher_uid, nickname, realname, mobile)
        class_info = {
            'course_name': course_name,
            'content_title': content_title,
            'start_time': start_time,
            'school_name': school_name,
            'student_number': student_number,
            'callback_key': callback_key,
            'teacher_info':teacher_info,
        }
        data.append(class_info)
    mysql_edu.closeDB()
    return data


@func_cache(expire=300)
def get_live_lesson_yesterday():
    day0 = datetime.date.today() - datetime.timedelta(1)
    day1 = datetime.date.today()
    time0 = int(time.mktime(time.strptime(str(day0), "%Y-%m-%d")))
    time1 = int(time.mktime(time.strptime(str(day1), "%Y-%m-%d")))
    edu_config = constants.MYSQL_EDU
    mysql_edu = MyDB(edu_config)
    sql = "select course_id,content_id,teacher_uid,start_time,callback_key \
            from live_lesson \
            where `start_time` between '%d' and '%d' and live_vendor = 1 \
            order by start_time" % (time0, time1)
    result = mysql_edu.execQuery(sql)
    x = 5
    lesson_list = [result[i:i + x] for i in range(0, len(result), x)]
    data = list()
    for lesson in lesson_list:
        course_id, content_id, teacher_uid, start_time, callback_key = lesson
        sql = "select course_name,school_name \
                from course co inner join school sc on co.school_id = sc.school_id \
                where `course_id` = '%d'" % course_id
        course_name, school_name = mysql_edu.execQuery(sql)
        sql = "select uid from course_auth_record where `course_id` = '%d'" % course_id
        list1 = mysql_edu.execQuery(sql)
        sql = "select student_uid from course_student where `course_id` = '%d'" % course_id
        list2 = mysql_edu.execQuery(sql)
        list3 = [x for x in list1 if x in list2]
        student_number = len(list1 + list2) - len(list3)
        sql = "select content_title from content where `content_id` = '%d'" % content_id
        res = mysql_edu.execQuery(sql)
        if len(res) == 0:
            continue
        content_title = res[0]
        sql = "SELECT count(*) FROM content_study_progress WHERE content_id = '%d' AND content_type = 1" % content_id
        real_number = mysql_edu.execQuery(sql)[0]
        if student_number == 0:
            class_rate = "0%%"
        else:
            class_rate = "%.2f%%" % ((real_number / student_number) * 100)
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
        class_info = {
            'course_name': course_name,
            'content_title': content_title,
            'start_time': start_time,
            'school_name': school_name,
            'student_number': student_number,
            'real_number': real_number,
            'class_rate': class_rate,
        }
        data.append(class_info)
    mysql_edu.closeDB()
    return data

