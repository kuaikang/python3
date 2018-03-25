import pymysql


def get_db():
    # 打开数据库连接
    try:
        db = pymysql.connect(
            host="localhost", user="root",
            password="123456", db="resource", port=3306,
            charset="utf8"
        )
        return db
    except Exception as e:
        print(e)


def item_repeat():
    db = get_db()
    cur = db.cursor()
    sql_item = "SELECT item_id from item GROUP BY question_id,`option` HAVING count(1) > 1"
    sql_delete = "delete from item WHERE item_id = '{0}'"
    cur.execute(sql_item)
    items = cur.fetchmany(10000)
    for item in items:
        cur.execute(sql_delete.format(item[0]))
        db.commit()
    cur.close()
    db.close()


def tag_repeat():
    sql_question = "SELECT question_id from tag  GROUP BY question_id HAVING count(1) > 1"
    sql_tag = "SELECT tag_id from tag WHERE question_id = '{0}'"
    sql_tag_delete = "DELETE FROM tag WHERE tag_id = '{0}'"
    db = get_db()
    cur = db.cursor()
    cur.execute(sql_question)
    question_ids = cur.fetchmany(20000)
    for question_id in question_ids:
        cur.execute(sql_tag.format(question_id[0]))
        tags = cur.fetchall()
        for tag in tags[:-1]:
            cur.execute(sql_tag_delete.format(tag[0]))
        db.commit()
    cur.close()
    db.close()


if __name__ == '__main__':
    item_repeat()
    # tag_repeat()