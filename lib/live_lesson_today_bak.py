#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 统计当天CClive直播课信息

from configs import constants
from lib.mydb import MyDB
from lib import write_excel
import time
import datetime

day1 = datetime.date.today()
day2 = datetime.date.today() + datetime.timedelta(1)
# day1 = "2019-12-29"
# day2 = "2019-12-30"
time1 = int(time.mktime(time.strptime(str(day1), "%Y-%m-%d")))
time2 = int(time.mktime(time.strptime(str(day2), "%Y-%m-%d")))
# print(time1, time2)
edu_config = constants.MYSQL_EDU
mysql_edu = MyDB(edu_config)
a = time.time()
sql = "select course_id,content_id,teacher_uid,start_time,callback_key,course_type \
        from live_lesson \
        where live_vendor = 5 and disabled = 0 and `start_time` between '%d' and '%d' \
        order by start_time, live_id" % (time1, time2)
result = mysql_edu.execQuery(sql)
b = time.time()
# print("查live_lesson %d" % (b - a))
x = 6
lesson_list = [result[i:i + x] for i in range(0, len(result), x)]
# print(lesson_list)
row0 = ["课程名称", "直播名称", "课程类型", "开课时间", "学院", "报名人数", "room_id", "讲师信息"]
values = list()
values.append(row0)
for lesson in lesson_list:
    course_id, content_id, teacher_uid, start_time, callback_key, course_type = lesson
    # print(course_id, content_id, teacher_uid, start_time, course_type)
    if course_type == 1:
        course_type = "正价课"
    elif course_type == 2:
        course_type = "公开课"
    elif course_type == 3:
        course_type = "微课"
    else:
        course_type = "直播未知类型%d" % course_type
    a = time.time()
    sql = "select course_name,school_name \
            from course co inner join school sc on co.school_id = sc.school_id \
            where `course_id` = '%d'" % course_id
    course_name, school_name = mysql_edu.execQuery(sql)
    if school_name == "测试学院":
        continue
    b = time.time()
    print("查course&school %d" % (b - a))
    # print(course_name, school_name)
    a = time.time()
    sql = "select uid from course_auth_record where `course_id` = '%d'" % course_id
    list1 = mysql_edu.execQuery(sql)
    b = time.time()
    print("查course_auth_record %d" % (b - a))
    a = time.time()
    sql = "select student_uid from course_student where `course_id` = '%d'" % course_id
    list2 = mysql_edu.execQuery(sql)
    b = time.time()
    print("查course_student %d" % (b - a))
    a = time.time()
    list3 = [x for x in list1 if x in list2]
    number = len(list1 + list2) - len(list3)
    b = time.time()
    print("计算报名人数 %d" % (b - a))
    # print(number)
    a = time.time()
    sql = "select content_title from content where `content_id` = '%d'" % content_id
    # print(mysql_edu.execQuery(sql))
    try:
        content_title = mysql_edu.execQuery(sql)[0]
    except:
        content_title = ''
    b = time.time()
    print("查content %d" % (b - a))
    # print(content_title)
    # sql = "SELECT count(*) FROM content_study_progress WHERE content_id = '%d' AND content_type = 1" % content_id
    # real_number = mysql_edu.execQuery(sql)[0]
    # print(real_number)
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
    # print(start_time)
    a = time.time()
    sql = "select nickname,realname,mobile from manager where `uid` = '%d'" % teacher_uid
    nickname, realname, mobile = mysql_edu.execQuery(sql)
    b = time.time()
    print("查manager %d" % (b - a))
    teacher_info = "%d / %s / %s / %s" % (teacher_uid, nickname, realname, mobile)
    # print(teacher_info)
    rowx = [course_name, content_title, course_type, start_time, school_name, number, callback_key, teacher_info]
    values.append(rowx)

mysql_edu.closeDB()
# print(values)
xls_name = "直播课信息%s.xls" % str(day1)
sheet_name = "直播课信息"
write_excel.write_excel_xls(xls_name, sheet_name, values)
