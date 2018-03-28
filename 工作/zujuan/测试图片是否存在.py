import pymysql
import os


def get_db():
    # 打开数据库连接
    try:
        db = pymysql.connect(
            host="123.206.227.74", user="root",
            password="exue2017", db="zujuan_spark_test", port=3306,
            charset="utf8"
        )
        return db
    except Exception as e:
        print(e)


def main(subject_key):
    db = get_db()
    cur = db.cursor()
    sql = "select answer_url from t_res_%s_question" % subject_key
    sql_tag = "select tag_url from t_res_%s_tag" % subject_key
    cur.execute(sql)
    result1 = cur.fetchall()
    for res in result1:
        if not os.path.exists(res[0]):
            print(res[0])
    cur.execute(sql_tag)
    result2 = cur.fetchall()
    for res in result2:
        if not os.path.exists(res[0]):
            print(res[0])
    cur.close()
    db.close()


if __name__ == '__main__':
    main("ls")