import pymysql
import time
import contextlib


# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='123.206.227.74', port=3306, user='root', password='exue2017', db='sit_exue_resource', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    finally:
        conn.commit()
        cur.close()
        conn.close()


def get_max(sql):
    with mysql() as cur:
        cur.execute(sql)
        return int(cur.fetchone().get('data'))


def get_subject_info(subject_key):
    with mysql() as cur:
        cur.execute('select * from t_res_subject WHERE summary_key = "{subject_key}"'.format(subject_key=subject_key))
        return cur.fetchone()


max_book_id = get_max("SELECT MAX(book_id) as data from t_res_book") + 100
max_unit_id = get_max("SELECT MAX(unit_id) as data from t_res_units") + 2000
max_chapter_id = get_max("SELECT MAX(chapter_id) as data from t_res_chapter") + 4000
create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
sql_book = "INSERT INTO t_res_book (`book_id`, `book_name`, `book_version`, `edition_id`, `subject_code`, `subject_name`, `create_time`, `finish`) " \
           "VALUES ('{book_id}', '{book_name}', '{book_version}', '{edition_id}', '{subject_code}', '{subject_name}', " \
           "'{create_time}', '1');"
sql_grade_book = "INSERT INTO t_res_graduate_book (`book_id`, `grade`, `semester`, `create_time`) " \
                 "VALUES ('{book_id}', '{grade}', '2', '{create_time}');"
sql_unit = "INSERT INTO t_res_units (`unit_id`, `unit_name`, `book_id`, `create_time`) " \
           "VALUES ('{unitId}', '{unitName}', '{bookId}', '{create_time}');"
sql_chapter = "INSERT INTO t_res_chapter (`chapter_id`, `chapter_name`, `unit_id`, `book_id`, `summary_key`, `create_time`, `finish`) " \
              "VALUES ('{chapter_id}', '{chapter_name}', '{unit_id}', '{book_id}', '{summary_key}', '{create_time}', '1');"


def insert_sql(index, summary_key, grade, book_name, book_version, edition_id):
    f_write = open("%s_sql.txt" % book_name, mode="w", encoding="utf8")
    book_id = max_book_id + index
    unit_id = max_unit_id + index * 50
    chapter_id = max_chapter_id + index * 100
    subject = get_subject_info(subject_key=summary_key)
    f_write.write(
        sql_book.format(book_id=book_id, book_name=book_name, book_version=book_version, edition_id=edition_id,
                        subject_code=subject.get('summary_code'), subject_name=subject.get('summary_name'),
                        create_time=create_time) + '\n')
    f_write.write(sql_grade_book.format(book_id=book_id, grade=grade, create_time=create_time) + '\n')  # 年级与课本关系
    f = open(book_name + ".txt", mode="r", encoding="utf8")
    unit = []
    data = f.readlines()
    f.close()
    for index, line in enumerate(data):
        if "_*_" in line:
            unit.append(index)
    unit.append(len(data))
    for index, item in enumerate(unit[:-1]):
        f_write.write(sql_unit.format(unitId=unit_id, unitName=data[item].strip().replace('_*_', ''),
                                      bookId=book_id, create_time=create_time) + '\n')  # 单元
        chapters = data[item + 1:unit[index + 1]]
        for chapter in chapters:
            f_write.write(sql_chapter.format(chapter_id=chapter_id, chapter_name=chapter.lstrip().strip(),
                                             unit_id=unit_id, book_id=book_id, summary_key=summary_key,
                                             create_time=create_time) + '\n')
            chapter_id += 1
        unit_id += 1


def main():
    # 序号,学科key,年级数字,书名,出版社,出版社id
    insert_sql(1, "yw", "1", "语文S版（新版）一年级下", "语文出版社", "155199")
    insert_sql(2, "yw", "1", "语文S版（新版）一年级上", "语文出版社", "155199")


if __name__ == '__main__':
    main()
