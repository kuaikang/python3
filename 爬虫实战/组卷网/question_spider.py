import requests
from urllib.parse import urlencode
import pymysql
import json
import re
import time


def get_db():
    # 打开数据库连接
    try:
        db = pymysql.connect(
            host="localhost", user="root",
            password="123456", db="zujuan", port=3306,
            charset="utf8"
        )
        return db
    except Exception as e:
        print(e)


def get_head():
    with open("conf", mode="r", encoding="utf8") as f:
        data = f.read().replace("\n", '').strip()
        return json.loads(data)


def get_chapter_id(cur, book_id):
    select_chapter_sql = "SELECT chapter_id from chapter WHERE book_id = '{}'".format(book_id)
    cur.execute(select_chapter_sql)
    data = cur.fetchall()
    return [item[0] for item in data]


head = get_head()
pattern = re.compile('.*?"answer":"(.*?)>*?"', re.S)


def get_answer_url(session, question_id):
    with session.get("http://www.zujuan.com/question/detail-%s.shtml" % question_id) as resp:
        if resp.status_code != 200:
            return None
        src = re.findall(pattern, resp.text)[0]
        return src


def get_question(categories, page):
    url = "http://www.zujuan.com/question/list?"
    req = {
        "categories": categories,
        "question_channel_type": "1",  # 题型
        "difficult_index": "",
        "grade_id[]": "0",
        "page": page,
        "kid_num": "",
        "exam_type": "",
        "sortField": "time",
        "_": "1521515844117"
    }
    grade7 = {"grade_id[]": "7"}
    grade8 = {"grade_id[]": "8"}
    grade9 = {"grade_id[]": "9"}
    params = urlencode(req) + "&" + urlencode(grade7) + "&" + urlencode(grade8) + "&" + urlencode(grade9)
    with requests.get(url + params, headers=head) as resp:
        if resp.status_code != 200:
            return None, None
        if len(resp.json().get("data")) == 0:
            return None, None
        questions = resp.json().get("data")[0].get('questions')
        total = resp.json().get("total")
        page = (total + 10 - 1) // 10
        return questions, page


insert_question = "INSERT INTO {subject}_question (question_id, context, question_type, difficult) " \
                  "VALUES ('{question_id}', '{context}', '{question_type}', '{difficult}')"
insert_chap_ques = 'INSERT INTO {0}_chapter_question (chapter_id, question_id) VALUES ("{1}", "{2}");'
insert_tag = 'INSERT INTO {0}_tag_question (tag_url,question_id) VALUES ("{1}", "{2}");'
insert_item = 'INSERT INTO {0}_item (context, `option`,`question_id`) VALUES ("{1}", "{2}","{3}");'
select_question = "select * from {}_question WHERE  question_id = {}"


def main(subject_key, book_id):
    db = get_db()
    db.autocommit(True)
    cur = db.cursor()
    session = requests.session()
    chapter_ids = get_chapter_id(cur, book_id)
    print(chapter_ids)
    for c_id in chapter_ids:
        for page in range(1, 1000):
            questions, total_page = get_question(c_id, page)
            print(c_id, total_page, page)
            if not questions: break
            for q in questions:
                if isinstance(q.get("options"), str):
                    continue
                if isinstance(q.get("options"), list):
                    continue
                try:
                    cur.execute(insert_chap_ques.format(subject_key, c_id, q.get("question_id")))  # 章节题目关系
                except Exception:
                    pass
                if not cur.execute(select_question.format(subject_key, q.get("question_id"))):
                    cur.execute(
                        insert_question.format(
                            subject=subject_key, question_id=q.get("question_id"),
                            context=pymysql.escape_string(q.get("question_text")),
                            question_type=q.get("question_type"),
                            difficult=q.get("difficult_index")
                        )
                    )
                    options = q.get("options")
                    for key, val in options.items():  # 选项
                        cur.execute(
                            insert_item.format(subject_key, pymysql.escape_string(val), key, q.get("question_id")))
                    cur.execute(insert_tag.format(subject_key, q.get("knowledge"), q.get("question_id")))
            if total_page == page:
                break  # 到达最后一页,退出循环
    session.close()
    cur.close()
    db.close()


if __name__ == '__main__':
    main('yw', '133566')
    main('yw', '544')
    main('yw', '545')
