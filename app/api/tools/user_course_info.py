#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 统计用户课程信息和数据

import time
from configs import constants
from lib.mydb import MyDB
from app import cache


def get_manager_info(mysql_edu, uid_list, role):
    teacher_list = []
    if len(uid_list) > 0:
        for uid in uid_list:
            sql = "SELECT uid,nickname,realname,mobile FROM manager WHERE uid = %s" % uid
            info_list = mysql_edu.execQuery(sql)
            teacher = {
                'role': role,
                'uid': info_list[0],
                'nickname': info_list[1],
                'realname': info_list[2],
                'mobile': info_list[3],
            }
            teacher_list.append(teacher)
    return teacher_list


@cache.memoize(timeout=300)
def get_course_info_by_mobile(mobile):
    edu_config = constants.MYSQL_EDU
    mysql_edu = MyDB(edu_config)
    sql = "SELECT cs.student_uid, cs.auth_type, cs.expired_at, cs.created_at, \
           c.course_id, c.course_name, c.school_id, c.type, c.expired_info, c.updated_at \
           FROM course_student cs INNER JOIN course c ON cs.course_id = c.course_id \
           WHERE cs.student_uid = (SELECT uid FROM student WHERE mobile = %d) \
           ORDER BY c.course_id DESC" % int(mobile)
    result = mysql_edu.execQuery(sql)
    x = 10
    course_list = [result[i:i + x] for i in range(0, len(result), x)]
    data = list()
    for course in course_list:
        # auth_type授权类型判断
        if course[1] == 1:
            auth_type = "后台授权"
        elif course[1] == 2:
            auth_type = "CRM授权"
        elif course[1] == 3:
            auth_type = "用户报名"
        elif course[1] == 4:
            auth_type = "星球"
        elif course[1] == 5:
            auth_type = "企业授权"
        elif course[1] == 9:
            auth_type = "第三方合作API接口"
        else:
            auth_type = str(course[1])
        # course_type课程类型判断
        if course[7] == 1:
            course_type = "大课"
        elif course[7] == 2:
            course_type = "宇宙公开课"
        elif course[7] == 3:
            course_type = "微课"
        elif course[7] == 4:
            course_type = "小课"
        elif course[7] == 5:
            course_type = "就业课"
        elif course[7] == 6:
            course_type = "内训课"
        elif course[7] == 7:
            course_type = "线下课"
        elif course[7] == 8:
            course_type = "普通公开课"
        elif course[7] == 9:
            course_type = "体验课"
        else:
            course_type = str(course[7])
        course_info = {
            'student_uid': course[0],
            'auth_type': auth_type,
            'expired_at': course[2],
            'created_at': course[3],
            'course_id': course[4],
            'course_name': course[5],
            'school_id': course[6],
            'course_type': course_type,
            'expired_info': course[8],
            'updated_at': course[9],
        }
        data.append(course_info)
    mysql_edu.closeDB()
    return data


@cache.memoize(timeout=300)
def get_course_auth_record_by_mobile(mobile):
    edu_config = constants.MYSQL_EDU
    mysql_edu = MyDB(edu_config)
    sql = "SELECT car.id, car.uid, car.map_id, car.map_type, car.course_id, c.course_name, \
           car.auth_status, car.xid, car.xtype, car.auth_from, car.created_at, car.updated_at \
           FROM course_auth_record car INNER JOIN course c ON car.course_id = c.course_id \
           WHERE uid = (SELECT uid FROM student WHERE mobile = %d) \
           ORDER BY id DESC" % int(mobile)
    result = mysql_edu.execQuery(sql)
    x = 12
    record_list = [result[i:i + x] for i in range(0, len(result), x)]
    data = list()
    for record in record_list:
        # map_type与uid对应的关联ID类型判断
        if record[3] == 1:
            map_type = "union_id"
        elif record[3] == 2:
            map_type = "uid"
        else:
            map_type = str(record[3])
        # auth_status授权状态判断
        if record[6] == 0:
            auth_status = "未完成"
        elif record[6] == 1:
            auth_status = "已完成"
        elif record[6] == 2:
            auth_status = "已取消"
        else:
            auth_status = str(record[6])
        # xtype授权的xid对应类型判断
        if record[8] == 1:
            xtype = "订单ID"
        else:
            xtype = str(record[8])
        # auth_status授权状态判断
        if record[9] == 1:
            auth_from = "CRM调用的微信授权"
        elif record[9] == 2:
            auth_from = "app或官网自然流量"
        elif record[9] == 3:
            auth_from = "小课授权"
        elif record[9] == 4:
            auth_from = "企业授权"
        else:
            auth_from = str(record[9])
        record_info = {
            'record_id': record[0],
            'uid': record[1],
            'map_id': record[2],
            'map_type': map_type,
            'course_id': record[4],
            'course_name': record[5],
            'auth_status': auth_status,
            'xid': record[7],
            'xtype': xtype,
            'auth_from': auth_from,
            'created_at': record[10],
            'updated_at': record[11],
        }
        data.append(record_info)
    mysql_edu.closeDB()
    return data


@cache.memoize(timeout=300)
def get_user_info_by_xid(xid_list):
    edu_config = constants.MYSQL_EDU
    mysql_edu = MyDB(edu_config)
    # xid = ','.join(["'%s'" % str(xid) for xid in xid_list])
    data = list()
    for xid in xid_list:
        sql = "SELECT car.id, car.uid, car.map_id, car.map_type, car.course_id, \
               c.course_name, car.auth_status, car.auth_from, car.xid, s.mobile \
               FROM (course_auth_record car INNER JOIN student s ON car.uid = s.uid) \
               INNER JOIN course c ON car.course_id = c.course_id \
               WHERE xid = '%s'" % xid
        result = mysql_edu.execQuery(sql)
        if result:
            # map_type与uid对应的关联ID类型判断
            if result[3] == 1:
                map_type = "union_id"
            elif result[3] == 2:
                map_type = "uid"
            else:
                map_type = str(result[3])
            # auth_status授权状态判断
            if result[6] == 0:
                auth_status = "未完成"
            elif result[6] == 1:
                auth_status = "已完成"
            elif result[6] == 2:
                auth_status = "已取消"
            else:
                auth_status = str(result[6])
            # auth_status授权状态判断
            if result[7] == 1:
                auth_from = "CRM调用的微信授权"
            elif result[7] == 2:
                auth_from = "app或官网自然流量"
            elif result[7] == 3:
                auth_from = "小课授权"
            elif result[7] == 4:
                auth_from = "企业授权"
            else:
                auth_from = str(result[7])
            record_info = {
                'record_id': result[0],
                'uid': result[1],
                'map_id': result[2],
                'map_type': map_type,
                'course_id': result[4],
                'course_name': result[5],
                'auth_status': auth_status,
                'auth_from': auth_from,
                'xid': result[8],
                'mobile': result[9],
            }
        else:
            record_info = {
                'xid': xid,
                'mobile': '',
            }
        data.append(record_info)
    mysql_edu.closeDB()
    return data


@cache.memoize(timeout=60)
def get_teacher_info_by_live_id(live_id):
    edu_config = constants.MYSQL_EDU
    mysql_edu = MyDB(edu_config)
    sql = "SELECT live_id,content_id,course_type,teacher_uid, real_start_time,real_end_time,\
          live_vendor,`status`, disabled, start_time, end_time \
          FROM live_lesson \
          WHERE callback_key = '%s'" % live_id
    result = mysql_edu.execQuery(sql)
    course_info = {}
    if result:
        # course_type课程类型判断
        if result[2] == 1:
            course_type = "正价课"
        elif result[2] == 2:
            course_type = "公开课"
        elif result[2] == 3:
            course_type = "微课"
        else:
            course_type = str(result[2])
        # live_vender直播类型判断
        if result[6] == 1:
            live_vendor = "CCLive"
        elif result[6] == 2:
            live_vendor = "classIn互动"
        elif result[6] == 3:
            live_vendor = "classin live直播"
        elif result[6] == 4:
            live_vendor = "CCLive+慧科云IM"
        elif result[6] == 5:
            live_vendor = "慧科云直播"
        else:
            live_vendor = str(result[6])
        # status直播课状态判断
        if result[7] == 0:
            status = "未开始"
        elif result[7] == 1:
            status = "直播中"
        elif result[7] == 2:
            status = "直播结束"
        elif result[7] == 3:
            status = "已生成回放"
        elif result[7] == 4:
            status = "回放异常"
        elif result[7] == 5:
            status = "备课中"
        else:
            status = str(result[7])
        # disabled判断是否为hky备课
        if result[8] == 0:
            disabled = "直播教室"
        elif result[8] == 1:
            disabled = "备课教室"
        else:
            disabled = str(result[8])
        course_sql = "SELECT cou.course_name,con.content_title \
                     FROM course cou INNER JOIN content con ON cou.course_id = con.course_id \
                     WHERE con.content_id = %d" % result[1]
        course = mysql_edu.execQuery(course_sql)
        course_info = {
            'live_id': result[0],
            'callback_key': live_id,
            'course_name': course[0],
            'course_type': course_type,
            'content_title': course[1],
            'live_vendor': live_vendor,
            'status': status,
            'disabled': disabled,
            'start_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(result[9])),
            'end_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(result[10])),
            'real_start_time': '未开始' if result[4] == 0 else time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(result[4])),
            'real_end_time': '未结束' if result[5] == 0 else time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(result[5])),
        }
        teacher_info = get_manager_info(mysql_edu, [result[3]], '老师')
        lla_sql = "SELECT assistant_uid FROM live_lesson_assistant WHERE live_id = %d" % result[0]
        lla_result = mysql_edu.execQuery(lla_sql)
        assistant_list = get_manager_info(mysql_edu, lla_result, '助教')
        teacher_info.extend(assistant_list)
        llct_sql = "SELECT class_teacher_uid FROM live_lesson_class_teacher WHERE live_id = %d" % result[0]
        llct_result = mysql_edu.execQuery(llct_sql)
        class_teacher = get_manager_info(mysql_edu, llct_result, '班主任')
        teacher_info.extend(class_teacher)
        course_info['teacher_info'] = teacher_info
    mysql_edu.closeDB()
    return course_info


if __name__ == '__main__':
    lid = 'live-842201207996416'
    course1 = get_teacher_info_by_live_id(lid)
    print(course1)
