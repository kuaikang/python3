import pymysql
from common.excel_util import read_excel
import uuid
import json


def get_db():
    # 打开数据库连接
    try:
        db = pymysql.connect(
            host='221.224.143.68', port=42580, user='root', password='root', db='topic_standard_test', charset='utf8'
        )
        return db
    except Exception as e:
        print(e)


db = get_db()
cur = db.cursor(pymysql.cursors.DictCursor)
db.autocommit(True)


def get_db_normal():
    # 打开数据库连接
    db = pymysql.connect(
        host="192.168.121.159", user="juzi_yxy",
        password="nimo)OKM", db="uat_exue_resource", port=42578,
        charset="utf8"
    )
    return db


db_normal = get_db_normal()
cur_normal = db.cursor(pymysql.cursors.DictCursor)


def uuid_get():
    return str(uuid.uuid4()).replace("-", "")


def select_tag():
    cur.execute("SELECT * FROM `t_res_tag` t LEFT JOIN t_res_tag g on t.id = g.parent_id "
                "WHERE t.subject_id = '020' and g.parent_id is null ORDER BY t.tag_name;")
    data = cur.fetchall()
    for item in data:
        print(item)


def get_tag(tag_name, subject):
    cur.execute("SELECT * FROM `t_res_tag` t LEFT JOIN t_res_tag g on t.id = g.parent_id "
                "WHERE t.subject_key ='%s' and g.parent_id is null and t.tag_name = '%s';" % (subject, tag_name))
    return cur.fetchall()


get_grade = """
        SELECT gb.grade from t_res_book b LEFT JOIN t_res_graduate_book gb on b.book_id = gb.book_id
        LEFT JOIN t_res_chapter c on c.book_id = b.book_id
        LEFT JOIN t_res_{subject}_question_chapter qc on qc.chapter_id = c.chapter_id
        WHERE qc.question_uuid in (SELECT question_uuid from t_res_{subject}_tag_question WHERE tag_id = '{tagId}') LIMIT 1;
"""


def write():
    f = open("yy.txt", mode="a", encoding="utf8")
    data = read_excel("C:/Users/开发/Desktop/知识点/【英语小学初中新旧知识点关联表】8.xls")
    for line in data:
        line[0] = str(line[0])[:-2]
        if "1" in line[0] or "2" in line[0]:
            if line[2] and line[2] in yw:
                cur.execute(get_grade.format(tagId=line[0]))
                data = cur.fetchone()
                if int(data.get('grade')) <= 6:
                    line[3] = 1
                if int(data.get('grade')) >= 7:
                    line[3] = 2


def main(subject, file_name):
    f_write = open("%s_map.txt" % subject, mode="a", encoding="utf8")
    data = read_excel("C:/Users/开发/Desktop/知识点/%s"%file_name)
    for line in data:
        line[0] = str(line[0])[:-2]
        if "1" in line[0] or "2" in line[0]:
            result = []
            for i in range(2, 4):
                if line[i]:
                    tag = get_tag(line[i], subject)
                    # 知识点名唯一
                    if len(tag) == 1:
                        result.append({tag[0].get('id'): tag[0].get('tag_name')})
                    # 知识点重名
                    if len(tag) > 1:
                        cur_normal.execute(get_grade.format(tagId=line[0], subject=subject))
                        res = cur_normal.fetchone()
                        if res:
                            if int(res.get('grade')) <= 6:
                                for t in tag:
                                    if t.get('period_id') == '1':
                                        result.append({t.get('id'): t.get('tag_name')})
                            if int(res.get('grade')) >= 7:
                                for t in tag:
                                    if t.get('period_id') == '1':
                                        result.append({t.get('id'): t.get('tag_name')})
            if result:
                print({line[0]: result})
                f_write.write(json.dumps({line[0]: result}, ensure_ascii=False))
                f_write.write("\n")


if __name__ == '__main__':
    # main('yw', '【语文小学初中新旧知识点关联表】.xlsx')
    main('yy', '【英语小学初中新旧知识点关联表】8.xls')
