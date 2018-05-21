from 基础知识.数据库存储.Mysql import pymysql_util
import pymysql
from 基础知识.文档操作.excel import excel_util


def get_db():
    # 打开数据库连接
    db = pymysql.connect(
        host="192.168.121.159", user="juzi_yxy",
        password="nimo)OKM", db="topic_standard", port=42578,
        charset="utf8"
    )
    return db


# 查询某个学科信息
# ('语文', '9', '语文北师版九上', '第二单元', '口技', 'edition_id', 'chapter_id')
def book_sql(subject_code):
    sql = "SELECT b.subject_name,gb.grade,b.book_name,u.unit_name,c.chapter_name,b.edition_id,c.chapter_id "
    sql += "from t_res_chapter c "
    sql += "LEFT JOIN t_res_units u on c.unit_id = u.unit_id "
    sql += "LEFT JOIN t_res_book b on c.book_id = b.book_id "
    sql += "LEFT JOIN t_res_graduate_book gb on c.book_id = gb.book_id "
    sql += "WHERE b.subject_code = '%s' group by c.chapter_id,gb.book_id"
    return sql % subject_code


# 查询新增题目数量
# def sql_count_new(subject_key):
#     sql = "SELECT qc.chapter_id,count(qc.question_uuid) from t_res_%s_question_chapter qc LEFT JOIN t_res_%s_question q "
#     sql += "on qc.question_uuid = q.uuid where type in ('2','11') "
#     sql += "and q.create_time > '2018-03-26 00:00:00' GROUP BY qc.chapter_id"
#     return sql % (subject_key, subject_key)


# 查询新增题目数量
def sql_count_new(subject_key):
    sql = "SELECT qc.chapter_id,count(qc.question_uuid) from t_res_%s_question_chapter qc " \
          "where create_time >= '2018-03-26' and create_time <= '2018-05-08 23:59:59' GROUP BY qc.chapter_id"
    return sql % subject_key


# 查询二月份之前录入题目数量
def sql_count_old(subject_key):
    sql = "SELECT qc.chapter_id,count(qc.question_uuid) from t_res_%s_question_chapter qc LEFT JOIN t_res_%s_question q "
    sql += "on qc.question_uuid = q.uuid where type in ('2','11') "
    sql += "and q.create_time < '2018-02-01 00:00:00' GROUP BY qc.chapter_id"
    return sql % (subject_key, subject_key)


def main(subject_key, subject_code):
    result_new = pymysql_util.find_all(db, sql_count_new(subject_key))  # '章节id','数量'
    result_old = pymysql_util.find_all(db, sql_count_old(subject_key))

    editor_sql = "SELECT edition_id,CONCAT(press_name,edition_name) from t_res_editor"
    editors = pymysql_util.find_all(db, editor_sql)
    sum = 0
    result_book = pymysql_util.find_all(db, book_sql(subject_code))
    # ('语文', '9', '语文北师版九上', '第二单元', '口技', 'edition_id', 'chapter_id')
    result_data = [["学科", "年级", "课本", "单元", "章节", "教材", "新增数量"]]
    for book in result_book:
        li = [book[0], book[1], book[2], book[3], book[4], 0, 0]
        for editor in editors:  # 教材
            if editor[0] == book[5]:
                li[5] = editor[1]
        for result in result_new:  # 二月新增数量
            if book[6] == result[0]:
                li[6] = result[1]
                sum += result[1]
        result_data.append(li)
    # excel_util.create_excel(result_data, "F:/导出/%s录入统计.xlsx" % result_book[0][0])
    return sum


if __name__ == '__main__':
    db = get_db()
    sub_key = ["yw", "sx", "yy", "dl", "hx", "ls", "wl", "zz", "sw", 'kx', "sp", "dd", "ty", "ms", "mu", "ps"]
    sub_name = ["010", "020", "030", "080", "060", "100", "050", "090", "070", "040", "160", "240", "110", "120", "130",
                "190"]
    data = 0
    for i in range(len(sub_key)):
        d = main(sub_key[i], sub_name[i])
        data += d
        print(sub_key[i], d)
    print(data)
