from 基础知识.文档操作.excel import excel_util
from common.mysql_util import mysql
import pymysql

conn = pymysql.connect(host="192.168.121.159", port=42578, user="juzi_emp", password="exue2018", db="uat_exue_resource",
                       charset="utf8")
cur = conn.cursor(cursor=pymysql.cursors.DictCursor)


def get_book(subject):
    """查询课本信息"""
    sql = "SELECT * from t_res_book b LEFT JOIN t_res_graduate_book gb on b.book_id = gb.book_id " \
          "LEFT JOIN t_res_editor e on b.edition_id = e.edition_id where b.subject_name = '{subject}' " \
          "and b.book_version = '人民教育出版社' GROUP BY b.book_id " \
          "ORDER BY CAST(gb.grade AS SIGNED) asc,b.edition_id,b.book_name;"
    cur.execute(sql.format(subject=subject))
    return cur.fetchall()


def question_count(subject, book_id):
    sql = "SELECT count(1) as num from t_res_{subject}_question_chapter qc where chapter_id in " \
          "(SELECT chapter_id from t_res_chapter c WHERE book_id = '{book_id}');"
    cur.execute(sql.format(subject=subject, book_id=book_id))
    return cur.fetchone()


def main(subject_key, subject_name):
    books = get_book(subject_name)
    result_data = [["学科", "年级", "版本", "课本", "题目数量"]]
    for book in books:
        data = [subject_name, book.get('grade'), book.get('press_name') + book.get('edition_name'),
                book.get('book_name'), 0]
        counts = question_count(subject_key, book.get('book_id'))
        data[-1] = counts.get('num')
        result_data.append(data)
    excel_util.create_excel(result_data, "F:/题目统计/%s人教版题目数量统计.xlsx" % subject_name)


if __name__ == '__main__':
    sub_key = ["yw", "sx", "yy", "dl", "hx", "ls", "wl", "zz", "sw", 'sp', 'dd', 'ps']
    sub_name = ["语文", "数学", "英语", "地理", "化学", "历史", "物理", "政治", "生物", "思想品德", "道德与法治", '品德与社会']
    for i in range(1):
        main(sub_key[i], sub_name[i])
    cur.close()
    conn.close()
