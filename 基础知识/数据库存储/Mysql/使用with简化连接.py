import pymysql
import contextlib


# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='127.0.0.1', port=3306, user='root', password='123456', db='lezhi', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    finally:
        conn.commit()
        cur.close()
        conn.close()


# 执行sql
with mysql() as cursor:
    print(cursor)
    row_count = cursor.execute("select * from book")
    row_1 = cursor.fetchone()
    print(row_count, row_1)
