import pymysql
import os
import contextlib


# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='123.206.227.74', port=3306, user='root', password='exue2017', db='zujuan_spark_test', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)
    conn.autocommit(True)
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    finally:
        conn.commit()
        cur.close()
        conn.close()


def path_exist(data, col):
    for res in data:
        if not os.path.exists(res.get(col)):
            print(res.get(col))


def main(subject_key):
    select_answer = "select answer_url from t_res_{subject_key}_question".format(subject_key=subject_key)
    select_tag = "select tag_url from t_res_{subject_key}_tag".format(subject_key=subject_key)
    with mysql() as cur:
        cur.execute(select_answer)
        path_exist(cur.fetchall(), "answer_url")
        cur.execute(select_tag)
        path_exist(cur.fetchall(), "tag_url")


if __name__ == '__main__':
    main("wl")
