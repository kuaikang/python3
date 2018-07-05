import pymysql
from 基础知识.文档操作.excel import excel_util


def get_db():
    # 打开数据库连接
    db = pymysql.connect(
        host="192.168.121.159", user="juzi_yxy",
        password="nimo)OKM", db="uat_exue_resource", port=42578,
        charset="utf8"
    )
    return db


db = get_db()
cur = db.cursor(pymysql.cursors.DictCursor)

sql = """SELECT COUNT(1) as num from t_res_{subject}_question_chapter qc LEFT JOIN t_res_yw_question q 
        on qc.question_uuid = q.uuid WHERE q.type in ('2','11') and qc.chapter_id in (
	    SELECT chapter_id from t_res_chapter c LEFT JOIN t_res_book b on c.book_id = b.book_id 
	    LEFT JOIN t_res_graduate_book gb on b.book_id = gb.book_id 
	    WHERE CAST(gb.grade AS SIGNED) <= 6 and b.edition_id = '{edition_id}');"""

select_editor = "select * from t_res_editor where press_name = '{press_name}' and edition_name = '{edition_name}'"


def main(subject, edition_id):
    cur.execute(sql.format(subject=subject, edition_id=edition_id))
    print(cur.fetchone().get('num'))


if __name__ == '__main__':
    with open("version.txt", mode="r", encoding="utf8") as f:
        for line in f.readlines():
            line = line.strip()
            press_name = line[:line.index("（")]
            edition_name = line[line.index("（"):]
            cur.execute(select_editor.format(press_name=press_name, edition_name=pymysql.escape_string(edition_name)))
            print(cur.fetchone())
        # main('yw')
