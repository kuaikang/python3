import pymysql
import requests
import threading
import re, time


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


def get_question_ids(cur,book_id,index):
    sql = "SELECT qc.question_id,q.answer_url from chapter_question qc LEFT JOIN chapter c on qc.chapter_id = c.chapter_id " \
          "LEFT JOIN question q on qc.question_id = q.question_id WHERE book_id = '%s' " \
          "and q.answer_url is null GROUP BY qc.question_id LIMIT %s,20"%(book_id,index)
    cur.execute(sql)
    return cur.fetchall()


def get_chapter_ids(question_id):
    sql = "SELECT chapter_id from chapter_question WHERE question_id = '%s'" % question_id
    cur.execute(sql)
    return cur.fetchall()


def update_question(db, cur, answer_url, question_id):
    sql = "UPDATE question SET answer_url = '{answer_url}' WHERE question_id = '{question_id}'"
    cur.execute(sql.format(answer_url=answer_url, question_id=question_id))
    db.commit()


def main(book_id,index):
    db = get_db()
    cur = db.cursor()
    question_ids = get_question_ids(cur, book_id,index)
    pattern = re.compile('.*?"answer":"(.*?)>*?"', re.S)
    sql = "UPDATE question SET answer_url = '{answer_url}' WHERE question_id = '{question_id}'"
    print("start")
    for question in question_ids:
        try:
            resp = requests.get("http://www.zujuan.com/question/detail-%s.shtml" % question[0])
        except Exception:
            resp = requests.get("http://www.zujuan.com/question/detail-%s.shtml" % question[0])
        src = re.findall(pattern, resp.text)[0]
        resp.close()
        cur.execute(sql.format(answer_url=src, question_id=question[0]))
        db.commit()
        time.sleep(0.2)
    cur.close()
    db.close()


if __name__ == '__main__':
    start = time.time()
    task = []
    for i in range(6):
        t = threading.Thread(target=main, args=("119441",i*20,))
        t.start()
        task.append(t)
    for t in task:
        t.join()
    print(time.time() - start)
