from 数据库存储.Mysql import pymysql_util
import pymysql
from 文档操作.excel import excel_util


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


# 查询某种题目类型的数量
def quest_sql(chapter_id, type):
    sql = "SELECT count(1) from t_res_yw_question_chapter qc "
    sql += "LEFT JOIN t_res_yw_question q on qc.question_uuid = q.uuid "
    sql += "WHERE chapter_id = '%s'"
    sql += "AND q.type = '%s'"
    return sql % (chapter_id, type)


def sql_chapter(chapter_id):
    sql = "SELECT count(1),qc.chapter_id from t_res_yw_question_chapter qc "
    sql += "LEFT JOIN t_res_yw_question q on qc.question_uuid = q.uuid "
    sql += "WHERE chapter_id = '%s' AND q.type = '11' HAVING COUNT(qc.question_uuid) > 0"
    return sql % chapter_id


# 查询章节下题目的数量(多选题)
def count_chapter_quest(subject_key):
    sql = "SELECT count(qc.question_uuid),qc.chapter_id from t_res_{0}_question_chapter qc  "
    sql += "LEFT JOIN t_res_{1}_question q on qc.question_uuid = q.uuid "
    sql += "where q.type = '12' GROUP BY qc.chapter_id HAVING count(qc.question_uuid) > 0"
    return sql.format(subject_key, subject_key)


def main(db, subject_key, subject_name):
    result = pymysql_util.find_all(db, book_sql(subject_name))
    # ('语文', '9', '语文北师版九上', '第二单元', '口技', 'edition_id', 'chapter_id')
    res = pymysql_util.find_all(db, count_chapter_quest(subject_key))  # ('chapterId','数量')
    res_dict = {}
    for re in res:
        res_dict[re[1]] = re[0]
    result_data = []
    for re in result:
        if re[6] in res_dict.keys():
            editor_sql = "SELECT CONCAT(press_name,edition_name) from t_res_editor WHERE edition_id = '%s'"
            editor = pymysql_util.find_one(db, editor_sql % re[5])
            data = [re[0], re[1], editor[0], re[2], re[3], re[4], res_dict[re[6]]]
            result_data.append(data)

    return result_data


if __name__ == '__main__':
    db = get_db()

    sub_key = ["yw", "sx", "yy", "dl", "hx", "ls", "wl", "zz", "sw"]
    sub_name = ["语文", "数学", "英语", "地理", "化学", "历史", "物理", "政治", "生物"]
    result = [["学科", "年级", "教材", "课本", "单元", "章节", "多选题数量"]]
    for i in range(9):
        data = main(db, sub_key[i], sub_name[i])
        for d in data:
            result.append(d)
    excel_util.create_excel(result, "多选题汇总2.xlsx")
