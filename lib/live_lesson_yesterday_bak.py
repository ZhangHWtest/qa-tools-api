#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 统计前一天CClive直播课质量报表

from configs import constants
from lib.mydb import MyDB
from lib import write_excel
import time
import datetime

day0 = datetime.date.today() - datetime.timedelta(1)
day1 = datetime.date.today()
# day0 = "2020-01-04"
# day1 = "2020-01-05"
time0 = int(time.mktime(time.strptime(str(day0), "%Y-%m-%d")))
time1 = int(time.mktime(time.strptime(str(day1), "%Y-%m-%d")))
# print(time1,time2)
edu_config = constants.MYSQL_EDU
mysql_edu = MyDB(edu_config)
sql = "select course_id,content_id,teacher_uid,start_time,callback_key, course_type \
        from live_lesson \
        where `start_time` live_vendor in (1,5) and disabled = 0 and between '%d' and '%d' \
        order by start_time, live_id" % (time0, time1)
result = mysql_edu.execQuery(sql)
x = 6
lesson_list = [result[i:i + x] for i in range(0, len(result), x)]
# print(lesson_list)
row0 = ["课程名称", "直播名称", "课程类型", "开课时间", "学院", "报名人数", "上课人数", "到课率",
        "异常反馈人数", "跟课人", "异常原因", "直播服务可靠性"]
values = list()
values.append(row0)
for lesson in lesson_list:
    course_id, content_id, teacher_uid, start_time, callback_key, course_type = lesson
    # print(course_id, content_id, teacher_uid, start_time, callback_key, course_type)
    if course_type == 1:
        course_type = "正价课"
    elif course_type == 2:
        course_type = "公开课"
    elif course_type == 3:
        course_type = "微课"
    else:
        course_type = "直播未知类型%d" % course_type
    sql = "select course_name,school_name \
            from course co inner join school sc on co.school_id = sc.school_id \
            where `course_id` = '%d'" % course_id
    course_name, school_name = mysql_edu.execQuery(sql)
    if school_name == "测试学院":
        continue
    # print(course_name, school_name)
    sql = "select uid from course_auth_record where `course_id` = '%d'" % course_id
    list1 = mysql_edu.execQuery(sql)
    sql = "select student_uid from course_student where `course_id` = '%d'" % course_id
    list2 = mysql_edu.execQuery(sql)
    list3 = [x for x in list1 if x in list2]
    number = len(list1 + list2) - len(list3)
    # print(number)
    sql = "select content_title from content where `content_id` = '%d'" % content_id
    try:
        content_title = mysql_edu.execQuery(sql)[0]
    except:
        content_title = ""
    # print(content_title)
    sql = "SELECT count(*) FROM content_study_progress WHERE content_id = '%d' AND content_type = 1" % content_id
    real_number = mysql_edu.execQuery(sql)[0]
    # print(real_number)
    if number == 0:
        class_rate = "0%%"
    else:
        class_rate = "%.2f%%" % ((real_number / number) * 100)
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
    # print(start_time)
    # sql = "select nickname,realname,mobile from manager where `uid` = '%d'" % teacher_uid
    # nickname, realname, mobile = mysql_edu.execQuery(sql)
    # teacher_info = "%d / %s / %s / %s" % (teacher_uid, nickname, realname, mobile)
    # print(teacher_info)
    rowx = [course_name, content_title, course_type, start_time, school_name, number, real_number, class_rate]
    values.append(rowx)

mysql_edu.closeDB()
# print(values)
xls_name = "直播课质量报表%s.xls" % str(day0)
sheet_name = "直播课质量信息"
write_excel.write_excel_xls(xls_name, sheet_name, values)

