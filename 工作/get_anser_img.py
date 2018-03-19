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


def get_question_ids(cur, index):
    sql = "SELECT question_id from question WHERE answer_url is null LIMIT %s,100" % index
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


def main(index):
    head = {
        "Cookie": "isRemove=1; _ga=GA1.2.1209185538.1520329414; _gid=GA1.2.1039098456.1521423702; PHPSESSID=lqh5c7ns81btc3fb1rrj8d26o4; _csrf=81bcf7fd71f377cb62c695f2f8d9b72ac359c7455ad6c524c154cb35b44b2446a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22BNYTnqAqjJvpjtaM3PdDHYWVOORLG3I9%22%3B%7D; isRemove=1; Hm_lvt_6de0a5b2c05e49d1c850edca0c13051f=1521177189,1521423696,1521423702,1521446251; chid=27e8704a451201531cc9941f6f3b709b7e13397751c04b090603ffdb0a56dfb9a%3A2%3A%7Bi%3A0%3Bs%3A4%3A%22chid%22%3Bi%3A1%3Bs%3A1%3A%222%22%3B%7D; xd=ff8cc2c663e498cf1fffa3d89aaa8ae9f68a128de39a6036c46ec0a0ff0b9459a%3A2%3A%7Bi%3A0%3Bs%3A2%3A%22xd%22%3Bi%3A1%3Bs%3A1%3A%221%22%3B%7D; Hm_lpvt_6de0a5b2c05e49d1c850edca0c13051f=1521446435"
    }
    db = get_db()
    cur = db.cursor()
    question_ids = get_question_ids(cur, index)
    pattern = re.compile('.*?"answer":"(.*?)>*?"', re.S)
    sql = "UPDATE question SET answer_url = '{answer_url}' WHERE question_id = '{question_id}'"
    for question in question_ids:
        resp = requests.get("http://www.zujuan.com/question/detail-%s.shtml" % question[0], headers=head)
        src = re.findall(pattern, resp.text)[0]
        resp.close()
        cur.execute(sql.format(answer_url=src, question_id=question[0]))
        db.commit()
    cur.close()
    db.close()


if __name__ == '__main__':
    start = time.time()
    task = []
    for i in range(20):
        t = threading.Thread(target=main, args=(i * 100,))
        t.start()
        task.append(t)
    for t in task:
        t.join()
    print(time.time() - start)
