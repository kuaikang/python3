import pymysql
from 基础知识.数据库存储.Mysql import pymysql_util


def get_db():
    # 打开数据库连接
    db = pymysql.connect(
        host="123.206.227.74", user="root",
        password="exue2017", db="topic_standard", port=3306,
        charset="utf8"
    )
    return db


if __name__ == '__main__':
    sql = "SELECT context from t_res_yw_question where uuid in (SELECT question_uuid FROM `t_res_yw_question_chapter` WHERE chapter_id = '010001001950929006001') and (type='2' or type='11')"
    results = pymysql_util.find_all(get_db(), sql)
    f = open("1.txt",mode="w",encoding="utf-8")
    for line in results:
        print("".join(line))
        f.write("".join(line))
        f.write("\n")
    f.close()