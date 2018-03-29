import json

if __name__ == '__main__':
    book_id = "150004001241060"
    summary_key = "xx"
    subject_name = "品德与社会"
    subject_code = "150"
    grade = "4"
    book_name = "信息技术川少版四上"
    book_version = "四川少年儿童出版社"
    edition_id = "155132"
    sql_book = "INSERT INTO t_res_book (`book_id`, `book_name`, `book_version`, `edition_id`, `subject_code`, `subject_name`, `cover`, `create_time`, `finish`) " \
               "VALUES ('{book_id}', '{book_name}', '{book_version}', '{edition_id}', '{subject_code}', '{subject_name}', " \
               "'http://dfs.res.jzexueyun.com/bookcover/200x200_003d248cab9bbbcbbad8eb2f3d30879c.jpg', '2017-11-15 10:41:31', '1');"
    sql_grade_book = "INSERT INTO t_res_graduate_book (`book_id`, `grade`, `semester`, `create_time`) " \
                     "VALUES ('{book_id}', '{grade}', '1', '2017-11-15 10:41:31');"
    sql_unit = "INSERT INTO t_res_units (`unit_id`, `unit_name`, `book_id`, `create_time`) " \
               "VALUES ('{unitId}', '{unitName}', '{bookId}', '2017-11-16 12:54:21');"
    sql_chapter = "INSERT INTO t_res_chapter (`chapter_id`, `chapter_name`, `unit_id`, `book_id`, `summary_key`, `create_time`, `finish`) " \
                  "VALUES ('{chapter_id}', '{chapter_name}', '{unit_id}', '{book_id}', '{summary_key}', '2017-11-16 12:54:21', '1');"
    print(sql_book.format(book_id=book_id,book_name=book_name,book_version=book_version,edition_id=edition_id,subject_code=subject_code,subject_name=subject_name))
    print(sql_grade_book.format(book_id=book_id, grade=grade)) # 年级与课本关系
    f = open("课本", mode="r", encoding="utf8")
    data = f.readline().strip()
    res = json.loads(data)
    units = res.get("wrapper").get("unitRecordList")
    for unit in units:
        print(sql_unit.format(unitId=unit["unitId"], unitName=unit["unitName"], bookId=book_id))  # 单元
    for unit in units:
        for chapter in unit["record"]:
            print(sql_chapter.format(chapter_id=chapter["unitId"], chapter_name=chapter["unitName"],  # 章节
                                     unit_id=unit["unitId"], book_id=book_id, summary_key=summary_key))
    f.close()

    # 课本,单元,章节,课本与年级的关系
