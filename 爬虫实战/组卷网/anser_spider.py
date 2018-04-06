import pymysql
import requests
import threading
import re


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


def get_question_ids(subject_key):
    db = get_db()
    cur = db.cursor()
    sql = "select question_id from {subject_key}_question where answer_url is null limit 3000"
    cur.execute(sql.format(subject_key=subject_key))
    data = cur.fetchall()
    cur.close()
    db.close()
    return data


pattern = re.compile('.*?"answer":"(.*?)>*?"', re.S)


def main(ids, subject):
    db = get_db()
    db.autocommit(True)
    cur = db.cursor()
    for question in ids:
        with requests.get("http://www.zujuan.com/question/detail-%s.shtml" % question[0]) as resp:
            if resp.status_code == 200:
                src = re.findall(pattern, resp.text)[0]
                cur.execute("update {}_question set answer_url = '{}' WHERE question_id = {}".
                            format(subject, src, question[0]))
    cur.close()
    db.close()


if __name__ == '__main__':
    question_ids = get_question_ids('yw')
    count = len(question_ids) // 10 + 1
    for i in range(8):
        t = threading.Thread(target=main, args=(question_ids[i * count:(i + 1) * count], 'yw',))
        t.start()
