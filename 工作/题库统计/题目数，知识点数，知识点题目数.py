from 基础知识.文档操作.excel import excel_util
from common.mysql_util import mysql


def book_count(subject_code):
    """查询某个学科信息"""
    with mysql(db="uat_exue_resource", host="192.168.121.159", user="juzi_yxy", password="nimo)OKM", port=42578) as cur:
        sql = "SELECT b.subject_name,gb.grade,b.book_name,u.unit_name,c.chapter_name,b.edition_id,c.chapter_id,"
        sql += "CONCAT(e.press_name,e.edition_name) as edition from t_res_chapter c "
        sql += "LEFT JOIN t_res_units u on c.unit_id = u.unit_id "
        sql += "LEFT JOIN t_res_book b on c.book_id = b.book_id "
        sql += "LEFT JOIN t_res_graduate_book gb on c.book_id = gb.book_id "
        sql += "LEFT JOIN t_res_editor e on b.edition_id = e.edition_id "
        sql += "WHERE b.subject_code = '{subject_code}' and b.book_name != '橘子学院营销培训' "
        cur.execute(sql.format(subject_code=subject_code))
        return cur.fetchall()


# 查询题目数量
def question_count(subject_key):
    with mysql(db="uat_exue_resource", host="192.168.121.159", user="juzi_yxy", password="nimo)OKM", port=42578) as cur:
        sql = """SELECT qc.chapter_id,count(qc.question_uuid) as num from t_res_%s_question_chapter qc 
              LEFT JOIN t_res_%s_question q on qc.question_uuid = q.uuid where type in ('2','11') 
              GROUP BY qc.chapter_id"""
        cur.execute(sql % (subject_key, subject_key))
    return cur.fetchall()


# 章节下带有知识点的题目数量
def chapter_question_tag(subject, subject_code):
    with mysql(db="uat_exue_resource", host="192.168.121.159", user="juzi_yxy", password="nimo)OKM", port=42578) as cur:
        sql = """SELECT c.chapter_id,count(DISTINCT tq.question_uuid) as num from t_res_{subject}_tag_question tq 
              LEFT JOIN t_res_{subject}_question_chapter qc on tq.question_uuid = qc.question_uuid
              LEFT JOIN t_res_{subject}_question q on tq.question_uuid = q.uuid
              LEFT JOIN t_res_chapter c on qc.chapter_id = c.chapter_id
              LEFT JOIN t_res_book b on c.book_id = b.book_id
              WHERE q.type in ('2','11') and b.subject_code = '{subject_code}' GROUP BY c.chapter_id;"""
        cur.execute(sql.format(subject_code=subject_code, subject=subject))
    return cur.fetchall()


def tag_count(subject_key):
    """统计章节知识点数量"""
    with mysql(db="uat_exue_resource", host="192.168.121.159", user="juzi_yxy", password="nimo)OKM", port=42578) as cur:
        sql = "SELECT qc.chapter_id,count(DISTINCT tq.tag_id) as num from t_res_{subject_key}_tag_question tq " \
              "LEFT JOIN t_res_{subject_key}_question_chapter qc " \
              "on tq.question_uuid = qc.question_uuid where qc.chapter_id is not null GROUP BY qc.chapter_id"
        cur.execute(sql.format(subject_key=subject_key))
        return cur.fetchall()


def main(subject_key, subject_code):
    sum = 0
    books = book_count(subject_code)
    tags = tag_count(subject_key)
    questions = question_count(subject_key)
    tag_questions = chapter_question_tag(subject_key, subject_code)
    result_data = [["学科", "年级", "版本", "课本", "单元", "章节", "知识点数量", "单选判断数量", "带有知识点题目数"]]
    for book in books:
        data = [book.get("subject_name"), book.get("grade"), book.get('edition'), book.get("book_name"),
                book.get('unit_name'), book.get('chapter_name'), 0, 0, 0]
        for tag in tags:
            if tag.get('chapter_id') == book.get('chapter_id'):
                data[-3] = tag.get('num')
                break
        for q in questions:
            if q.get('chapter_id') == book.get('chapter_id'):
                data[-2] = q.get('num')
                sum += q.get('num')
                break
        for t in tag_questions:
            if t.get('chapter_id') == book.get('chapter_id'):
                data[-1] = t.get('num')
                break
        result_data.append(data)
    if sum > 0:
        excel_util.create_excel(result_data, "F:/导出/大杂烩/%s大杂烩统计.xlsx" % books[0].get('subject_name'))
    return sum


if __name__ == '__main__':
    sub_key = ["yw", "sx", "yy", "dl", "hx", "ls", "wl", "zz", "sw", 'kx', "sp", "dd", "ty", "ms", "mu", "ps", "xx"]
    sub_code = ["010", "020", "030", "080", "060", "100", "050", "090", "070", "040", "160", "240", "110", "120", "130",
                "190", "150"]
    for i in range(len(sub_key)):
        main(sub_key[i], sub_code[i])
