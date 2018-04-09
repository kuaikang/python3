import requests
import pymysql
import os
import re
import time
import contextlib


# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='localhost', port=3333, user='root', password='kuaikang', db='lezhi', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    finally:
        conn.commit()
        cur.close()
        conn.close()


head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    "Cookie": "JSESSIONID=9055057E8E6CB6BF0CF7699E7B386767; JYY-Cookie-20480=EELHKIMAFAAA; Hm_lvt_83bc962335f6e0741154dacdbf8c0c62=1523265323; Hm_lvt_3b2b90b968014bee5b24ff51962ad7ac=1523265323; name=value; UM_distinctid=162a9b07b9438b-0504262b8498df-3a61430c-1fa400-162a9b07b956a7; CNZZDATA1253279410=872901333-1523261327-http%253A%252F%252Fwww.jiaoxueyun.cn%252F%7C1523261327; Hm_lpvt_3b2b90b968014bee5b24ff51962ad7ac=1523265398; Hm_lpvt_83bc962335f6e0741154dacdbf8c0c62=1523265399"
}


def valid_name(name):
    reg = re.compile(r'[\\/:*?"<>|\r\n]+')
    valid = reg.findall(name)
    if valid:
        for v in valid:
            name = name.replace(v, '')
    return name


def download(book_id):
    proxies = {'http': 'http://39.134.10.17:8080'}
    url = "http://www.jiaoxueyun.cn/res-view!download.do?resource_id=%s"
    with mysql() as cursor:
        sql = "SELECT * from resource where book_id = '{book_id}' order by chapter_id".format(book_id=book_id)
        cursor.execute(sql)
        data = cursor.fetchall()
    for res in data:
        path = "F:/resource/%s/%s/%s/%s/%s" % (
            res.get('course_name'), res.get('grade_name'), res.get('version_name'), valid_name(res.get('book_name')),
            valid_name(res.get('chapter_name')))
        if not os.path.exists(path):
            os.makedirs(path)
        res_path = "%s/%s.%s" % (path, valid_name(res.get('resource_name')), res.get('type').lower())
        if os.path.exists(res_path):
            continue
        try:
            resp = requests.get(url=url % res.get('resource_id'), headers=head, stream=True)
        except Exception:
            continue
        if '登录' not in resp.text or "资" not in resp.text:
            print(resp.url)
            print(res_path)
            f = open(res_path, mode="wb")
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
            f.close()
        resp.close()
        time.sleep(0.5)


if __name__ == '__main__':
    book_ids = ['2870']
    for book_id in book_ids:
        download(book_id)
