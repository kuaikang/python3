def main(book_id, summary_key, subject_name, subject_code, grade, book_name, book_version, edition_id, file_name,unit_id,chapter_id):
    sql_book = "INSERT INTO t_res_book (`book_id`, `book_name`, `book_version`, `edition_id`, `subject_code`, `subject_name`, `cover`, `create_time`, `finish`) " \
               "VALUES ('{book_id}', '{book_name}', '{book_version}', '{edition_id}', '{subject_code}', '{subject_name}', " \
               "'http://dfs.res.jzexueyun.com/bookcover/200x200_003d248cab9bbbcbbad8eb2f3d30879c.jpg', '2017-11-15 10:41:31', '1');"
    sql_grade_book = "INSERT INTO t_res_graduate_book (`book_id`, `grade`, `semester`, `create_time`) " \
                     "VALUES ('{book_id}', '{grade}', '1', '2017-11-15 10:41:31');"
    sql_unit = "INSERT INTO t_res_units (`unit_id`, `unit_name`, `book_id`, `create_time`) " \
               "VALUES ('{unitId}', '{unitName}', '{bookId}', '2017-11-16 12:54:21');"
    sql_chapter = "INSERT INTO t_res_chapter (`chapter_id`, `chapter_name`, `unit_id`, `book_id`, `summary_key`, `create_time`, `finish`) " \
                  "VALUES ('{chapter_id}', '{chapter_name}', '{unit_id}', '{book_id}', '{summary_key}', '2017-11-16 12:54:21', '1');"

    print(sql_book.format(book_id=book_id, book_name=book_name, book_version=book_version, edition_id=edition_id,
                          subject_code=subject_code, subject_name=subject_name))
    print(sql_grade_book.format(book_id=book_id, grade=grade))  # 年级与课本关系
    f = open(file_name, mode="r", encoding="utf8")
    unit = []
    data = f.readlines()
    f.close()
    for index, line in enumerate(data):
        if "单元" in line:
            unit.append(index)
    unit.append(len(data))
    for index, item in enumerate(unit[:-1]):
        print(sql_unit.format(unitId="0" + str(unit_id), unitName=data[item].strip(), bookId=book_id))  # 单元
        chapters = data[item + 1:unit[index + 1]]
        for chapter in chapters:
            print(sql_chapter.format(chapter_id="0" + str(chapter_id), chapter_name=chapter.lstrip().strip(),
                                     unit_id="0" + str(unit_id), book_id=book_id, summary_key=summary_key))
            chapter_id += 1
        unit_id += 1


if __name__ == '__main__':
    book_id = "010001009866358"
    summary_key = "yw"
    subject_name = "语文"
    subject_code = "010"
    grade = "7"
    book_name = "语文北师大版七下"
    book_version = "北京师范大学出版社"
    edition_id = "019016"
    unit_id = 10001009863001
    chapter_id = 10001009830001
    # main(book_id, summary_key, subject_name, subject_code, grade, book_name, book_version, edition_id, "语文北师大版七下.txt")

    main("010001009866355", "yw", "语文", "010", "7", "语文苏教版七下", "江苏凤凰教育出版社", "047100", "语文苏教版七下.txt",10001009863001,10001009830001)
    main("010001009866356", "yw", "语文", "010", "7", "语文语文版七下", "语文出版社", "048100", "语文语文版七下.txt",10001009864001,10001009840001)
    main("010001009866357", "yw", "语文", "010", "7", "语文北师大版七下", "北京师范大学出版社", "019016", "语文北师大版七下.txt",10001009865001,10001009850001)
    main("010001009866358", "sp", "思想品德", "160", "7", "思想品德北师大版七下", "北京师范大学出版社", "019016", "思想品德北师大版七下.txt", 10001009866001,10001009860001)
    main("010001009866359", "sp", "思想品德", "160", "8", "思想品德北师大版八下", "北京师范大学出版社", "019016", "思想品德北师大版八下.txt",10001009867001, 10001009870001)
