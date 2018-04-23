import contextlib
import pymysql
from 基础知识.文档操作.excel import excel_util


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


# 查询某个学科信息
# ('语文', '9', '语文北师版九上', '第二单元', '口技', 'edition_id', 'chapter_id')
def book_count(subject_name):
    with mysql() as cur:
        sql = "SELECT b.subject_name,gb.grade,b.book_name,u.unit_name,c.chapter_name,b.edition_id,c.chapter_id,CONCAT(e.press_name,e.edition_name) as edition "
        sql += "from t_res_chapter c "
        sql += "LEFT JOIN t_res_units u on c.unit_id = u.unit_id "
        sql += "LEFT JOIN t_res_book b on c.book_id = b.book_id "
        sql += "LEFT JOIN t_res_graduate_book gb on c.book_id = gb.book_id "
        sql += "LEFT JOIN t_res_editor e on b.edition_id = e.edition_id "
        sql += "WHERE b.subject_name = '{subject_name}' and b.book_name != '橘子学院营销培训' "
        cur.execute(sql.format(subject_name=subject_name))
        return cur.fetchall()


# 统计章节知识点数量
def tag_count(subject_key):
    with mysql() as cur:
        sql = "SELECT qc.chapter_id,count(DISTINCT tq.tag_id) as num from t_res_{subject_key}_tag_question tq " \
              "LEFT JOIN t_res_{subject_key}_question_chapter qc " \
              "on tq.question_uuid = qc.question_uuid where qc.chapter_id is not null GROUP BY qc.chapter_id"
        cur.execute(sql.format(subject_key=subject_key))
        return cur.fetchall()


def main(subject_name, subject_key):
    books = book_count(subject_name)
    tags = tag_count(subject_key)
    result_data = [["学科", "年级", "版本", "课本", "单元", "章节", "知识点数量"]]
    for book in books:
        data = [book.get("subject_name"), book.get("grade"), book.get('edition'), book.get("book_name"),
                book.get('unit_name'), book.get('chapter_name'), 0]
        for tag in tags:
            if tag.get('chapter_id') == book.get('chapter_id'):
                data[-1] = tag.get('num')
        result_data.append(data)
    excel_util.create_excel(result_data, "%s知识点统计.xlsx" % subject_name)


if __name__ == '__main__':
    main('语文', 'yw')
