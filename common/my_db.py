"""
接口用例测试查询测试数据库测试结果对比，
现在支持查询mysql，进行对比
"""
import pymysql


def curse_db(host, port, user, password, database):
    """链接数据库，code为1即链接成功，error为错误信息，con为返回的链接的实例"""
    try:
        con = pymysql.connect(host=host, port=port, user=user, password=password, db=database)
        return {'code': 1, 'con': con}
    except Exception as e:
        return {'code': 0, 'error': str(e)}


def execute_mysql(con, sql):
    """执行数据库的sql，code为1即执行sql成功，result为返回结果"""
    try:
        with con.cursor() as conn:
            conn.execute(sql)
            result = conn.fetchall()
        return {'code': 1, 'result': result}
    except Exception as e:
        return {'code': 0, 'error': str(e)}
