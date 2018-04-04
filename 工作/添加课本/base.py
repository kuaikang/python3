import pymysql


def get_db_sit():
    # 打开数据库连接
    try:
        db = pymysql.connect(
            host="123.206.227.74", user="root",
            password="exue2017", db="topic_standard", port=3306,
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
    return int(max_book_id) + 1


def get_max_unit_id():
    db = get_db_sit()
    cur = db.cursor()
    cur.execute("SELECT MAX(unit_id) from t_res_units")
    max_unit_id = cur.fetchone()[0]
    cur.close()
    db.close()
    return int(max_unit_id) + 1


def get_max_chapter_id():
    db = get_db_sit()
    cur = db.cursor()
    cur.execute("SELECT MAX(chapter_id) from t_res_chapter")
    max_chapter_id = cur.fetchone()[0]
    cur.close()
    db.close()
    return int(max_chapter_id) + 1


def insert_sql(index, summary_key, subject_name, subject_code, grade, book_name, book_version,
               edition_id, file_name):
    sql_book = "INSERT INTO t_res_book (`book_id`, `book_name`, `book_version`, `edition_id`, `subject_code`, `subject_name`, `cover`, `create_time`, `finish`) " \
               "VALUES ('{book_id}', '{book_name}', '{book_version}', '{edition_id}', '{subject_code}', '{subject_name}', " \
               "'http://dfs.res.jzexueyun.com/bookcover/200x200_003d248cab9bbbcbbad8eb2f3d30879c.jpg', '2018-04-04 10:41:31', '1');"
    sql_grade_book = "INSERT INTO t_res_graduate_book (`book_id`, `grade`, `semester`, `create_time`) " \
                     "VALUES ('{book_id}', '{grade}', '1', '2018-04-04 10:41:31');"
    sql_unit = "INSERT INTO t_res_units (`unit_id`, `unit_name`, `book_id`, `create_time`) " \
               "VALUES ('{unitId}', '{unitName}', '{bookId}', '2018-04-04 12:54:21');"
    sql_chapter = "INSERT INTO t_res_chapter (`chapter_id`, `chapter_name`, `unit_id`, `book_id`, `summary_key`, `create_time`, `finish`) " \
                  "VALUES ('{chapter_id}', '{chapter_name}', '{unit_id}', '{book_id}', '{summary_key}', '2018-04-04 12:54:21', '1');"
    book_id = get_max_book_id() + index
    unit_id = get_max_unit_id() + index * 50
    chapter_id = get_max_chapter_id() + index * 100
    print(sql_book.format(book_id=book_id, book_name=book_name, book_version=book_version, edition_id=edition_id,
                          subject_code=subject_code, subject_name=subject_name))
    print(sql_grade_book.format(book_id=book_id, grade=grade))  # 年级与课本关系
    f = open(file_name, mode="r", encoding="utf8")
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
    insert_sql(1, "kx", "科学", "040", "3", "科学教科版三上", "教育科学出版社", "037100", "0404/科学教科版三上.txt")
    insert_sql(2, "kx", "科学", "040", "3", "科学教科版三上", "教育科学出版社", "037100", "0404/科学教科版三上.txt")

    insert_sql(3, "yw", "语文", "010", "1", "语文人教版一上", "人民教育出版社", "001001", "0404/语文人教版(标准)一上.txt")
    insert_sql(4, "yw", "语文", "010", "1", "语文人教版一下", "人民教育出版社", "001001", "0404/语文人教版(标准)一下.txt")
    insert_sql(5, "yw", "语文", "010", "2", "语文人教版二上", "人民教育出版社", "001001", "0404/语文人教版(标准)二上.txt")
    insert_sql(6, "yw", "语文", "010", "2", "语文人教版二下", "人民教育出版社", "155217", "0404/语文人教版(部编)二下.txt")

    insert_sql(7, "yw", "语文", "010", "1", "语文北师大版一上", "北京师范大学出版社", "019016", "0404/语文北师大版(标准)一上.txt")
    insert_sql(8, "yw", "语文", "010", "1", "语文北师大版一下", "北京师范大学出版社", "019016", "0404/语文北师大版(标准)一下.txt")

    insert_sql(9, "yw", "语文", "010", "2", "语文北师大版二上", "北京师范大学出版社", "019016", "0404/语文北师大版(标准)二上.txt")

    insert_sql(10, "yw", "语文", "010", "7", "语文北师大版七上", "北京师范大学出版社", "019016", "0404/语文北师大版七上.txt")
    insert_sql(11, "yw", "语文", "010", "8", "语文北师大版八上", "北京师范大学出版社", "019016", "0404/语文北师大版八上.txt")

    insert_sql(12, "yw", "语文", "010", "1", "语文苏教版一上", "江苏凤凰教育出版社", "047100", "0404/语文苏教版(标准)一上.txt")
    insert_sql(13, "yw", "语文", "010", "1", "语文苏教版一下", "江苏凤凰教育出版社", "047100", "0404/语文苏教版(标准)一下.txt")
    insert_sql(14, "yw", "语文", "010", "2", "语文苏教版二上", "江苏凤凰教育出版社", "047100", "0404/语文苏教版(标准)二上.txt")

    insert_sql(15, "yw", "语文", "010", "7", "语文苏教版七上", "江苏凤凰教育出版社", "047100", "0404/语文苏教版七上.txt")
    insert_sql(16, "yw", "语文", "010", "8", "语文苏教版八上", "江苏凤凰教育出版社", "047100", "0404/语文苏教版八上.txt")

    insert_sql(17, "yw", "语文", "010", "1", "语文语文版一上", "语文出版社", "019100", "0404/语文语文S版一上.txt")
    insert_sql(18, "yw", "语文", "010", "1", "语文语文版一下", "语文出版社", "019100", "0404/语文语文S版一下.txt")
    insert_sql(19, "yw", "语文", "010", "2", "语文语文版二下", "语文出版社", "019100", "0404/语文语文S版二下.txt")

    insert_sql(20, "yw", "语文", "010", "7", "语文语文版七上", "语文出版社", "048100", "0404/语文语文版七上.txt")
    insert_sql(21, "yw", "语文", "010", "8", "语文语文版八上", "语文出版社", "048100", "0404/语文语文版八上.txt")


if __name__ == '__main__':
    main()
