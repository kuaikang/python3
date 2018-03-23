import pymysql


def get_db():
    # 打开数据库连接
    try:
        db = pymysql.connect(
            host="localhost", user="root",
            password="kuaikang", db="lezhi", port=3333,
            charset="utf8"
        )
        return db
    except Exception as e:
        print(e)


def insert_grade():
    db = get_db()
    cur = db.cursor()
    sql_grade = "INSERT INTO grade (`grade_id`, `grade_name`) VALUES ('%s', '%s');"
    dic = {'G04': '一年级', 'G05': '二年级', 'G06': '三年级', 'G07': '四年级', 'G08': '五年级', 'G09': '六年级', 'G10': '七年级',
           'G11': '八年级', 'G12': '九年级', 'G13': '高一', 'G14': '高二', 'G15': '高三'}
    for key, val in dic.items():
        cur.execute(sql_grade % (key, val))
        db.commit()
    cur.close()
    db.close()


def insert_book():
    sql = "INSERT INTO book (`book_id`, `book_name`, `course_id`, `version_id`, `grade_id`) VALUES ('%s', '%s', '%s', '%s', '%s');"
    db = get_db()
    cur = db.cursor()
    f = open("book.txt", mode="r", encoding="utf8")
    for line in f.readlines():
        line = line.split(",")
        cur.execute(sql % (line[3], line[4], line[1], line[2], line[0]))
        db.commit()
    f.close()
    cur.close()
    db.close()


if __name__ == '__main__':

    insert_book_sql = "INSERT INTO chapter (`chapter_id`, `chapter_name`, `book_id`) VALUES ('%s', '%s', '%s');"
