import pymysql


def get_db_res():
    # 打开数据库连接
    db = pymysql.connect(
        host="123.206.227.74", user="root",
        password="exue2017", db="topic_standard_test", port=3306,
        charset="utf8"
    )
    return db


def get_db_zujuan():
    # 打开数据库连接
    try:
        db = pymysql.connect(
            host="192.168.121.40", user="root",
            password="001233", db="kuaik", port=3306,
            charset="utf8"
        )
        return db
    except Exception as e:
        print(e)


def main(res_book_id, zujuan_book_id):
    db = get_db_res()
    cur = db.cursor()
    db1 = get_db_zujuan()
    cur1 = db1.cursor()
    sql = "SELECT chapter_name,chapter_id FROM t_res_chapter WHERE book_id = '%s'"
    cur.execute(sql % book_id)
    data = cur.fetchall()
    result = []
    for d in data:
        sql = "SELECT chapter_id from chapter WHERE book_id = '%s' and chapter_name = '%s'"
        cur1.execute(sql % (zujuan_book_id, d[0]))
        res = cur1.fetchone()
        if res:
            result.append([d[0], d[1], res[0]])
        else:
            print(d[0])
    print(result)
    print(len(result))
    cur.close()
    cur1.close()
    db.close()
    db1.close()


if __name__ == '__main__':
    book_id = '100007001620337'
    zujuan_book_id = "119441"
    main(book_id, zujuan_book_id)
