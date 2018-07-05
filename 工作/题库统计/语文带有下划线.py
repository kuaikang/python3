import pymysql
from common.excel_util import create_excel


def get_db():
    # 打开数据库连接
    db = pymysql.connect(
        host="192.168.121.159", user="juzi_yxy",
        password="nimo)OKM", db="topic_standard", port=42578,
        charset="utf8"
    )
    return db


db = get_db()
cur = db.cursor(pymysql.cursors.DictCursor)


def questions():
    sql = "SELECT * from t_res_yw_question WHERE context like '%加线%' or context like '%下划线%' or context like '%划线%';"
    cur.execute(sql)
    return cur.fetchall()


def other_info(question_uuid):
    sql = """
        SELECT gb.grade,b.book_name,b.book_version,e.edition_name from t_res_yw_question_chapter qc
        LEFT JOIN t_res_chapter c ON qc.chapter_id = c.chapter_id
        LEFT JOIN t_res_book b ON c.book_id = b.book_id
        LEFT JOIN t_res_graduate_book gb on b.book_id = gb.book_id
        LEFT JOIN t_res_editor e on b.edition_id = e.edition_id
        WHERE qc.question_uuid = '{question_uuid}' LIMIT 1;"""
    cur.execute(sql.format(question_uuid=question_uuid))
    return cur.fetchone()


def items(question_uuid):
    sql = "SELECT * from t_res_yw_item WHERE question_uuid = '{question_uuid}';"
    cur.execute(sql.format(question_uuid=question_uuid))
    return cur.fetchall()


def main():
    f = open("1.html",encoding="utf8",mode="a")
    f.write('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title></head><body>')
    question_list = questions()
    for q in question_list:
        info = other_info(q.get('uuid'))
        data = [info.get('grade')+'年级', info.get('book_name'), info.get('book_version'), info.get('edition_name')]
        f.write("  ".join(data))
        f.write("<br/>")
        item = items(q.get('uuid'))
        for t in item:
            f.write(t.get('content'))
            f.write("<br/>")
        f.write("<br/>")
        f.write("<br/>")
    f.write('</body></html')
    f.close()


if __name__ == '__main__':
    # main()
    print(len(questions()))