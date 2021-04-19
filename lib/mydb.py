#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import datetime
from configs import constants


class MyDB(object):

    def __init__(self, config):
        self.config = config
        self._conn = self.connectDB()
        if self._conn:
            self._cursor = self._conn.cursor()

    def connectDB(self):
        """链接数据库"""
        conn = False
        try:
            conn = pymysql.connect(**self.config)
            print("数据库连接成功")
        except Exception as e:
            print("连接数据库失败, %s" % e)
        else:
            return conn
        
    def execQuery(self, sql):
        """执行查询类语句"""
        res = []
        try:
            self._cursor.execute(sql)
            data = self._cursor.fetchall()
            for l in data:
                for i in range(len(l)):
                    if isinstance(l[i], datetime.datetime):
                        x = l[i].strftime('%Y-%m-%d %H:%M:%S')
                    elif isinstance(l[i], datetime.date):
                        x = l[i].strftime("%Y-%m-%d")
                    else:
                        x = l[i]
                    res.append(x)
        except Exception as e:
            print("查询失败, %s" % e)
        else:
            return res
        
    def execNonQuery(self, sql):
        """执行非查询类语句"""
        flag = False
        try:
            self._cursor.execute(sql)
            self._conn.commit()
            flag = True
        except Exception as e:
            flag = False
            self._conn.rollback()
            print("执行失败, %s" % e)
        else:
            return flag
        
    def closeDB(self):
        if self._conn:
            try:
                if type(self._cursor) == 'object':
                    self._cur.close()
                if type(self._conn) == 'object':
                    self._conn.close()
                    print("数据库连接断开")
            except:
                raise("关闭异常, %s,%s" % (type(self._cursor), type(self._conn)))


if __name__ == '__main__':
    config = constants.MYSQL_PASSPORT
    mysql = MyDB(config)
    mobile = "13520738000"
    sql = "select * from user where mobile = '%s'" % mobile
    # unionid = "oBB9psyVE9OybGkrl_7q1tI-Xrgc"
    # sql = "select uid from user_wechat_map where unionid = '%s'" % unionid
    res = mysql.execQuery(sql)
    uid = res[0]
    print(uid)
    mysql.closeDB()
