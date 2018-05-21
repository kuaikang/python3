from 基础知识.文档操作.excel import excel_util
import pymysql

conn = pymysql.connect(host='192.168.121.159', port=42578, user='juzi_emp', passwd="exue2018",
                       db="uat_exue_resource", charset="utf8")
cur = conn.cursor(pymysql.cursors.DictCursor)


def book_count(subject_name):
    """查询某个学科信息"""
    sql = "SELECT b.subject_name,gb.grade,b.book_name,u.unit_name,c.chapter_name,b.edition_id,c.chapter_id," \
          "CONCAT(e.press_name,e.edition_name) as edition from t_res_chapter c LEFT JOIN t_res_units u on c.unit_id = u.unit_id " \
          "LEFT JOIN t_res_book b on c.book_id = b.book_id LEFT JOIN t_res_graduate_book gb on c.book_id = gb.book_id " \
          "LEFT JOIN t_res_editor e on b.edition_id = e.edition_id WHERE b.subject_name = '{subject_name}' " \
          "and b.book_name != '橘子学院营销培训' "
    cur.execute(sql.format(subject_name=subject_name))
    return cur.fetchall()


def resource_count(subject):
    cur.execute(
        "SELECT chapter_id,count(file_name) as sum from t_exue_resource_{subject} GROUP BY chapter_id".format(
            subject=subject))
    return {item.get('chapter_id'): item.get('sum') for item in cur.fetchall()}


def main(subject, subject_name):
    books = book_count(subject_name)
    resource = resource_count(subject)
    res = [["学科", '年级', '出版社', '课本', '单元', '章节', '课件数量']]
    for book in books:
        data = [book.get('subject_name'), book.get('grade'), book.get('edition'), book.get('book_name'),
                book.get('unit_name'), book.get('chapter_name'), 0]
        if resource.get(book.get('chapter_id')):
            data[-1] = resource.get(book.get('chapter_id'))
        res.append(data)
    excel_util.create_excel(res, "F:/导出/%s课件统计.xlsx" % subject_name)


if __name__ == '__main__':
    subjects = {"yw": "语文", "sx": "数学", "yy": "英语", "zz": "政治", "ls": "历史", "dl": "地理", "wl": "物理", "hx": "化学",
                "sw": "生物", "kx": "科学", "sp": "思想品德"}
    for key, val in subjects.items():
        main(key, val)
    conn.close()
    cur.close()
