import pymysql
import requests
import threading
import re
import contextlib
import sys


# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='localhost', port=3333, user='root', password='kuaikang', db='kuaik', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)
    conn.autocommit(True)
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    finally:
        conn.commit()
        cur.close()
        conn.close()


def get_question_ids(subject_key):
    with mysql() as cur:
        sql = "select question_id from {subject_key}_question where answer_url is null limit 2000"
        cur.execute(sql.format(subject_key=subject_key))
        data = cur.fetchall()
        return data


pattern = re.compile('.*?"answer":"(.*?)>*?"', re.S)


def main(ids, subject):
    with mysql() as cur:
        for question in ids:
            with requests.get("http://www.zujuan.com/question/detail-%s.shtml" % question.get('question_id')) as resp:
                if resp.status_code == 200:
                    src = re.findall(pattern, resp.text)[0]
                    print(src)
                    cur.execute("update {}_question set answer_url = '{}' WHERE question_id = {}".
                                format(subject, src, question.get('question_id')))


if __name__ == '__main__':
    subject_key = sys.argv[1]
    subject_keys = ["yw", "sx", "yy", "dl", "hx", "ls", "wl", "zz", "sw", 'kx', "sp", "dd", "ty", "ms", "mu"]
    if subject_key not in subject_keys:
        print("subject_key error")
    question_ids = get_question_ids(subject_key)
    count = len(question_ids) // 5 + 1
    for i in range(5):
        t = threading.Thread(target=main, args=(question_ids[i * count:(i + 1) * count], subject_key,))
        t.start()
