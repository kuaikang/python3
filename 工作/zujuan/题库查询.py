from 数据库存储.Mysql import pymysql_util
import pymysql


def get_db():
    # 打开数据库连接
    db = pymysql.connect(
        host="123.206.227.74", user="root",
        password="exue2017", db="topic_standard", port=3306,
        charset="utf8"
    )
    return db


def create_excel(db, subject_name):
    sql = ""
    pymysql_util.find_all(db,sql)