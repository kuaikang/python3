import pymysql
from common.mysql_util import mysql
from common.excel_util import create_excel


def get_db():
    # 打开数据库连接
    db = pymysql.connect(
        host="192.168.121.159", user="juzi_yxy",
        password="nimo)OKM", db="uat_exue_resource", port=42578,
        charset="utf8"
    )
    return db


sql = """SELECT * from t_res_{subject}_tag_question tq LEFT JOIN t_res_{subject}_tag t on tq.tag_id = t.tag_id
    WHERE tq.question_uuid in (
    SELECT qc.question_uuid from t_res_graduate_book gb LEFT JOIN t_res_chapter c on gb.book_id = c.book_id
    LEFT JOIN t_res_{subject}_question_chapter qc on c.chapter_id = qc.chapter_id where gb.grade = {grade}) 
    GROUP BY t.tag_id"""


def grade_tag(cur, subject, grade):
    cur.execute(sql.format(subject=subject, grade=grade))
    return cur.fetchall()


def main(subject):
    result = [['年级', '知识点']]
    with mysql(host="192.168.121.159", user="juzi_yxy", password="nimo)OKM", db="uat_exue_resource", port=42578) as cur:
        for grade in range(1, 10):
            data = grade_tag(cur, subject, grade)
            for d in data:
                result.append([grade, d.get('tag_name')])
    create_excel(result, "F:/导出/%s知识点.xlsx" % subjects.get(subject))


subjects = {
    "yw": "语文", "sx": "数学", "yy": "英语", "zz": "政治", "ls": "历史", "dl": "地理", "wl": "物理", "hx": "化学", "sw": "生物"
}

if __name__ == '__main__':
    for key in subjects.keys():
        main(key)
