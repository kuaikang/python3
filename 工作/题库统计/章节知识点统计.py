from 基础知识.文档操作.excel import excel_util
from common.mysql_util import mysql


def book_count(subject_name):
    """查询某个学科信息"""
    with mysql(db="sit_exue_resource") as cur:
        sql = "SELECT b.subject_name,gb.grade,b.book_name,u.unit_name,c.chapter_name,b.edition_id,c.chapter_id,"
        sql += "CONCAT(e.press_name,e.edition_name) as edition from t_res_chapter c "
        sql += "LEFT JOIN t_res_units u on c.unit_id = u.unit_id "
        sql += "LEFT JOIN t_res_book b on c.book_id = b.book_id "
        sql += "LEFT JOIN t_res_graduate_book gb on c.book_id = gb.book_id "
        sql += "LEFT JOIN t_res_editor e on b.edition_id = e.edition_id "
        sql += "WHERE b.subject_name = '{subject_name}' and b.book_name != '橘子学院营销培训' "
        cur.execute(sql.format(subject_name=subject_name))
        return cur.fetchall()


def tag_count(subject_key):
    """统计章节知识点数量"""
    with mysql(db="sit_exue_resource") as cur:
        sql = "SELECT qc.chapter_id,count(DISTINCT tq.tag_id) as num from t_res_{subject_key}_tag_question tq " \
              "LEFT JOIN t_res_{subject_key}_question_chapter qc " \
              "on tq.question_uuid = qc.question_uuid where qc.chapter_id is not null GROUP BY qc.chapter_id"
        cur.execute(sql.format(subject_key=subject_key))
        return cur.fetchall()


def main(subject_key, subject_name):
    books = book_count(subject_name)
    tags = tag_count(subject_key)
    result_data = [["学科", "年级", "版本", "课本", "单元", "章节", "知识点数量"]]
    for book in books:
        data = [book.get("subject_name"), book.get("grade"), book.get('edition'), book.get("book_name"),
                book.get('unit_name'), book.get('chapter_name'), 0]
        for tag in tags:
            if tag.get('chapter_id') == book.get('chapter_id'):
                data[-1] = tag.get('num')
                break
        result_data.append(data)
    excel_util.create_excel(result_data, "知识点/%s知识点统计.xlsx" % subject_name)


if __name__ == '__main__':
    sub_key = ["yw", "sx", "yy", "dl", "hx", "ls", "wl", "zz", "sw"]
    sub_name = ["语文", "数学", "英语", "地理", "化学", "历史", "物理", "政治", "生物"]
    for i in range(len(sub_key)):
        main(sub_key[i], sub_name[i])
