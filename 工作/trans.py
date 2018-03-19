import requests
import pymysql


def get_db():
    # 打开数据库连接
    try:
        db = pymysql.connect(
            host="192.168.121.40", user="root",
            password="001233", db="kuaik", port=3306,
            charset="utf8"
        )
        return db
    except Exception as e:
        print(e)


def get_question_ids(cur, chapter_id):
    sql = "SELECT question_id from chapter_question WHERE chapter_id = '%s' limit 1"
    cur.execute(sql % chapter_id)
    return cur.fetchall()


def get_question(cur, question_id):
    sql = "SELECT context,type,difficult from question WHERE question_id = '%s'"
    cur.execute(sql % question_id)
    return cur.fetchall()


def get_tag(cur, tag_id):
    sql = "SELECT tag_name from tag WHERE question_id = '%s'"
    cur.execute(sql % tag_id)
    return cur.fetchone()


def get_item(cur, question_id):
    sql = "SELECT content,`option` from item WHERE question_id = '%s'"
    cur.execute(sql % question_id)
    return cur.fetchall()


if __name__ == '__main__':
    db = get_db()
    cur = db.cursor()
    currentSubject = "yw"
    import_Chapter = ""
    zujuan_chapter = "630"
    question_ids = get_question_ids(cur, zujuan_chapter)
    for question_id in question_ids:
        question = get_question(cur, question_id[0])
        for q in question:  # context,type,difficult
            req = {"currentSubject": currentSubject, "questionContent": q[0], "importChapterId": import_Chapter, "questionType": "11"}
            tag = get_tag(cur, question_id[0])  # tag[0]
            req["tagUrl"] = tag[0]
            req["answerUrl"] = "http://www.zujuan.com/question/detail-%s.shtml"% question_id[0]
            items = get_item(cur, question_id[0])
            item = []
            for it in items:  # content,`option`
                item.append({"content":it[0],"option":it[1]})
            req["items"] = item
            print(req)
    cur.close()
    db.close()