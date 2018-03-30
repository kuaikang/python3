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
            host="localhost", user="root",
            password="kuaikang", db="kuaik", port=3333,
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
        name = d[0].replace(' ', '').replace(' ', '')
        cur1.execute(sql % (zujuan_book_id, name))
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
    # book_id, zuJuan_book_id = '070007001041100', "4583"  # 生物人教版七上
    # book_id, zuJuan_book_id = '070007002041100', "4584"  # 生物人教版七下
    # book_id, zuJuan_book_id = '070008001041100', "4586"  # 生物人教版八上
    # book_id, zuJuan_book_id = '070008002041100', "4587"  # 生物人教版八下
    # book_id, zuJuan_book_id = '060009001022100', "90991"  # 化学人教版九上
    book_id, zuJuan_book_id = '060009002022100', "90992"  # 化学人教版九下
    main(book_id, zuJuan_book_id)
