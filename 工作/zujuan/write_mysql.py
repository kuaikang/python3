import pymysql
from 数据库存储.Mysql import pymysql_util


def get_db():
    # 打开数据库连接
    db = pymysql.connect(
        host="localhost", user="root",
        password="123456", db="kuaik", port=3306,
        charset="utf8"
    )
    return db


if __name__ == '__main__':
    db = get_db()
    f = open("cz.txt", mode="r", encoding="utf8")
    data = []
    for line in f.readlines():
        li = line.split(",")
        sql = "INSERT INTO book (subject_name,subject_code,editor_name,editor_id, book_name,book_id) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"
        pymysql_util.insert_one(db, sql % (li[0], li[1], li[2], li[3], li[4], li[5].strip()))
    f.close()