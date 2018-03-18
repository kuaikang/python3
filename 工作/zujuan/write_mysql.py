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


def insert_book():
    db = get_db()
    cur = db.cursor()
    f = open("gz.txt", mode="r", encoding="utf8")
    for line in f.readlines():
        li = line.split(",")
        sql = "INSERT INTO `resource`.`book` (subject_name,subject_id,editor_name,editor_id, book_name,book_id,period) "
        sql += "VALUES ('%s', '%s', '%s', '%s', '%s', '%s','%s')"
        result = cur.execute(sql % (li[0], li[1], li[2], li[3], li[4], li[5].strip(), 3))
    db.commit()
    f.close()


def insert_unit(file_name):
    db = get_db()
    cur = db.cursor()
    f = open(file_name, mode="r", encoding="utf8")
    for line in f.readlines():
        li = line.split(",")
        try:
            sql = 'INSERT INTO `resource`.`unit` (`unit_id`, `unit_name`, `book_id`) VALUES ("{0}", "{1}", "{2}")'
            cur.execute(sql.format(li[0], li[1], li[2].strip()))
            db.commit()
        except Exception:
            print(sql.format(li[0], li[1], li[2].strip()))
    f.close()


def insert_chapter(file_name):
    db = get_db()
    cur = db.cursor()
    f = open(file_name, mode="r", encoding="utf8")
    for line in f.readlines():
        li = line.split(",")
        try:
            sql = 'INSERT INTO `resource`.`chapter` (`chapter_id`, `chapter_name`, `unit_id`, `book_id`) ' \
                  'VALUES ("{0}", "{1}", "{2}", "{3}")'
            cur.execute(sql.format(li[0], li[1], li[2], li[3].strip()))
            db.commit()
        except Exception:
            print(sql.format(li[0], li[1], li[2], li[3].strip()))
    f.close()


if __name__ == '__main__':
    # insert_unit("xx_unit.txt")
    # insert_unit("cz_unit.txt")
    # insert_unit("gz_unit.txt")

    # insert_chapter("xx_chapter.txt")
    # insert_chapter("cz_chapter.txt")
    # insert_chapter("gz_chapter.txt")

    pass