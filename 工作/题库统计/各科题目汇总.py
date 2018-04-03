from 基础知识.数据库存储.Mysql import pymysql_util
import pymysql
from 基础知识.文档操作.excel import excel_util


def get_db():
    # 打开数据库连接
    db = pymysql.connect(
        host="123.206.227.74", user="root",
        password="exue2017", db="sit_exue_resource", port=3306,
        charset="utf8"
    )
    return db


# 查询某个学科信息
# ('语文', '9', '语文北师版九上', '第二单元', '口技', 'edition_id', 'chapter_id')
def book_sql(subject_name):
    sql = "SELECT b.subject_name,gb.grade,b.book_name,u.unit_name,c.chapter_name,b.edition_id,c.chapter_id "
    sql += "from t_res_chapter c "
    sql += "LEFT JOIN t_res_units u on c.unit_id = u.unit_id "
    sql += "LEFT JOIN t_res_book b on c.book_id = b.book_id "
    sql += "LEFT JOIN t_res_graduate_book gb on c.book_id = gb.book_id "
    sql += "WHERE b.subject_name = '%s'"
    return sql % subject_name


# 查询三月份录入题目数量
def sql_count_new(subject_key):
    sql = "SELECT qc.chapter_id,count(qc.question_uuid) from t_res_%s_question_chapter qc LEFT JOIN t_res_%s_question q "
    sql += "on qc.question_uuid = q.uuid where type in ('2','11') "
    sql += "and q.create_time > '2018-03-01 00:00:00' and q.create_time < '2018-03-31 23:59:59' GROUP BY qc.chapter_id"
    return sql % (subject_key, subject_key)


# 查询二月份之前录入题目数量
def sql_count_old(subject_key):
    sql = "SELECT qc.chapter_id,count(qc.question_uuid) from t_res_%s_question_chapter qc LEFT JOIN t_res_%s_question q "
    sql += "on qc.question_uuid = q.uuid where type in ('2','11') "
    sql += "and q.create_time < '2018-02-01 00:00:00' GROUP BY qc.chapter_id"
    return sql % (subject_key, subject_key)


def main(subject_key, subject_name):
    result_new = pymysql_util.find_all(db, sql_count_new(subject_key))  # '章节id','数量'
    result_old = pymysql_util.find_all(db, sql_count_old(subject_key))

    editor_sql = "SELECT edition_id,CONCAT(press_name,edition_name) from t_res_editor"
    editors = pymysql_util.find_all(db, editor_sql)

    result_book = pymysql_util.find_all(db, book_sql(subject_name))
    # ('语文', '9', '语文北师版九上', '第二单元', '口技', 'edition_id', 'chapter_id')
    result_data = [["学科", "年级", "课本", "单元", "章节", "教材", "学乐数量", "三月新增数量"]]
    for book in result_book:
        li = [book[0], book[1], book[2], book[3], book[4], 0, 0, 0]
        for editor in editors:  # 教材
            if editor[0] == book[5]:
                li[5] = editor[1]
        for result in result_old:  # 学乐云数量
            if book[6] == result[0]:
                li[6] = result[1]
        for result in result_new:  # 二月新增数量
            if book[6] == result[0]:
                li[7] = result[1]
        result_data.append(li)
    excel_util.create_excel(result_data, "%s(单选判断)统计.xlsx" % subject_name)


if __name__ == '__main__':
    db = get_db()
    sub_key = ["yw", "sx", "yy", "dl", "hx", "ls", "wl", "zz", "sw", 'kx', "sp", "dd", "ty", "ms", "mu"]
    sub_name = ["语文", "数学", "英语", "地理", "化学", "历史", "物理", "政治", "生物", "科学", "思想品德", "道德与法治", "体育", "美术", "音乐"]

    for i in range(len(sub_key)):
        main(sub_key[i], sub_name[i])
