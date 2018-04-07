import pymysql


def get_db():
    # 打开数据库连接
    db = pymysql.connect(
        host="localhost", user="root",
        password="123456", db="lezhi", port=3306,
        charset="utf8"
    )
    return db


if __name__ == '__main__':
    conn = get_db()
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 将游标设置为字典类型
    cur.execute("select * from book limit 10")
    print(cur.fetchone())
