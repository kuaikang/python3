import json
import time

if __name__ == '__main__':
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    book_id = "100008002240901"
    summary_key = "ls"
    subject_name = "历史"
    subject_code = "100"
    grade = "8"
    book_name = "历史人教版八下"
    book_version = "人民教育出版社"
    edition_id = "155217"
    sql_book = "INSERT INTO t_res_book (`book_id`, `book_name`, `book_version`, `edition_id`, `subject_code`, `subject_name`, `cover`, `create_time`, `finish`) " \
               "VALUES ('{book_id}', '{book_name}', '{book_version}', '{edition_id}', '{subject_code}', '{subject_name}', " \
               "'http://dfs.res.jzexueyun.com/bookcover/200x200_003d248cab9bbbcbbad8eb2f3d30879c.jpg', '{create_time}', '1');"
    sql_grade_book = "INSERT INTO t_res_graduate_book (`book_id`, `grade`, `semester`, `create_time`) " \
                     "VALUES ('{book_id}', '{grade}', '2', '{create_time}');"
    sql_unit = "INSERT INTO t_res_units (`unit_id`, `unit_name`, `book_id`, `create_time`) " \
               "VALUES ('{unitId}', '{unitName}', '{bookId}', '{create_time}');"
    sql_chapter = "INSERT INTO t_res_chapter (`chapter_id`, `chapter_name`, `unit_id`, `book_id`, `summary_key`, `create_time`, `finish`) " \
                  "VALUES ('{chapter_id}', '{chapter_name}', '{unit_id}', '{book_id}', '{summary_key}', '{create_time}', '1');"
    print(sql_book.format(book_id=book_id, book_name=book_name, book_version=book_version, edition_id=edition_id,
                          subject_code=subject_code, subject_name=subject_name, create_time=create_time))
    print(sql_grade_book.format(book_id=book_id, grade=grade, create_time=create_time))  # 年级与课本关系
    f = open("课本", mode="r", encoding="utf8")
    data = f.readline().strip()
    res = json.loads(data)
    units = res.get("wrapper").get("unitRecordList")
    for unit in units:
        print(sql_unit.format(unitId=unit["unitId"], unitName=unit["unitName"], bookId=book_id,
                              create_time=create_time))  # 单元
    for unit in units:
        for chapter in unit["record"]:
            print(sql_chapter.format(chapter_id=chapter["unitId"], chapter_name=chapter["unitName"],  # 章节
                                     unit_id=unit["unitId"], book_id=book_id, summary_key=summary_key,
                                     create_time=create_time))
    f.close()

    # 课本,单元,章节,课本与年级的关系
