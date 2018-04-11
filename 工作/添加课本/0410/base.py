import pymysql


def get_db_sit():
    # 打开数据库连接
    try:
        db = pymysql.connect(
            host="123.206.227.74", user="root",
            password="exue2017", db="sit_exue_resource", port=3306,
            charset="utf8"
        )
        return db
    except Exception as e:
        print(e)


def get_max_book_id():
    db = get_db_sit()
    cur = db.cursor()
    cur.execute("SELECT MAX(book_id) from t_res_book")
    max_book_id = cur.fetchone()[0]
    cur.close()
    db.close()
    return int(max_book_id) + 100


def get_max_unit_id():
    db = get_db_sit()
    cur = db.cursor()
    cur.execute("SELECT MAX(unit_id) from t_res_units")
    max_unit_id = cur.fetchone()[0]
    cur.close()
    db.close()
    return int(max_unit_id) + 2000


def get_max_chapter_id():
    db = get_db_sit()
    cur = db.cursor()
    cur.execute("SELECT MAX(chapter_id) from t_res_chapter")
    max_chapter_id = cur.fetchone()[0]
    cur.close()
    db.close()
    return int(max_chapter_id) + 4000


def insert_sql(index, summary_key, subject_name, subject_code, grade, book_name, book_version, edition_id):
    sql_book = "INSERT INTO t_res_book (`book_id`, `book_name`, `book_version`, `edition_id`, `subject_code`, `subject_name`, `cover`, `create_time`, `finish`) " \
               "VALUES ('{book_id}', '{book_name}', '{book_version}', '{edition_id}', '{subject_code}', '{subject_name}', " \
               "'http://dfs.res.jzexueyun.com/bookcover/200x200_003d248cab9bbbcbbad8eb2f3d30879c.jpg', '2018-04-10 10:41:32', '1');"
    sql_grade_book = "INSERT INTO t_res_graduate_book (`book_id`, `grade`, `semester`, `create_time`) " \
                     "VALUES ('{book_id}', '{grade}', '1', '2018-04-10 10:41:32');"
    sql_unit = "INSERT INTO t_res_units (`unit_id`, `unit_name`, `book_id`, `create_time`) " \
               "VALUES ('{unitId}', '{unitName}', '{bookId}', '2018-04-10 10:41:32');"
    sql_chapter = "INSERT INTO t_res_chapter (`chapter_id`, `chapter_name`, `unit_id`, `book_id`, `summary_key`, `create_time`, `finish`) " \
                  "VALUES ('{chapter_id}', '{chapter_name}', '{unit_id}', '{book_id}', '{summary_key}', '2018-04-10 10:41:32', '1');"
    book_id = get_max_book_id() + index
    unit_id = get_max_unit_id() + index * 50
    chapter_id = get_max_chapter_id() + index * 100
    print(sql_book.format(book_id=book_id, book_name=book_name, book_version=book_version, edition_id=edition_id,
                          subject_code=subject_code, subject_name=subject_name))
    print(sql_grade_book.format(book_id=book_id, grade=grade))  # 年级与课本关系
    f = open(book_name + ".txt", mode="r", encoding="utf8")
    unit = []
    data = f.readlines()
    f.close()
    for index, line in enumerate(data):
        if "_*_" in line:
            unit.append(index)
    unit.append(len(data))
    for index, item in enumerate(unit[:-1]):
        print(sql_unit.format(unitId=unit_id, unitName=data[item].strip().replace('_*_', ''),
                              bookId=book_id))  # 单元
        chapters = data[item + 1:unit[index + 1]]
        for chapter in chapters:
            print(sql_chapter.format(chapter_id=chapter_id, chapter_name=chapter.lstrip().strip(),
                                     unit_id=unit_id, book_id=book_id, summary_key=summary_key))
            chapter_id += 1
        unit_id += 1


def main():
    # insert_sql(1, "kx", "科学", "040", "3", "科学冀教版三上", "河北教育出版社", "020100")
    # insert_sql(2, "kx", "科学", "040", "3", "科学冀教版三下", "河北教育出版社", "020100")
    #
    # insert_sql(3, "kx", "科学", "040", "4", "科学冀教版四上", "河北教育出版社", "020100")
    # insert_sql(4, "kx", "科学", "040", "4", "科学冀教版四下", "河北教育出版社", "020100")
    #
    # insert_sql(5, "kx", "科学", "040", "5", "科学冀教版五上", "河北教育出版社", "020100")
    # insert_sql(6, "kx", "科学", "040", "5", "科学冀教版五下", "河北教育出版社", "020100")
    #
    # insert_sql(7, "kx", "科学", "040", "6", "科学冀教版六上", "河北教育出版社", "020100")
    # insert_sql(8, "kx", "科学", "040", "6", "科学冀教版六下", "河北教育出版社", "020100")

    insert_sql(1, "ls", "历史", "100", "7", "历史北师大版七上", "北京师范大学出版社", "019016")
    insert_sql(2, "ls", "历史", "100", "8", "历史北师版八上", "北京师范大学出版社", "019016")

    insert_sql(3, "ps", "品德与社会", "190", "7", "品德与社会北师版七上", "北京师范大学出版社", "019016")
    insert_sql(4, "ps", "品德与社会", "190", "8", "品德与社会北师版八上", "北京师范大学出版社", "019016")


if __name__ == '__main__':
    main()
