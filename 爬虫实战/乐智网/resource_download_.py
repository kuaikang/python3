import requests
import pymysql
import os
import re
import time
import contextlib
import threading


# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='localhost', port=3306, user='root', password='123456', db='lezhi', charset='utf8'):
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
    "Cookie":"wP_h=716e702abcf2ca100644575e712c0d5214902c22; JSESSIONID=9C2B5299D522CD0A0BFCE046BBC41033; JYY-Cookie-20480=EGLHKIMAFAAA; Hm_lvt_83bc962335f6e0741154dacdbf8c0c62=1523280888; Hm_lvt_3b2b90b968014bee5b24ff51962ad7ac=1523280888; name=value; UM_distinctid=162aa9ec3d88e7-0d761b415d9b65-3a61430c-100200-162aa9ec3d96a9; CNZZDATA1253279410=587411053-1523277541-http%253A%252F%252Fwww.jiaoxueyun.cn%252F%7C1523277541; Hm_lpvt_3b2b90b968014bee5b24ff51962ad7ac=1523280957; Hm_lpvt_83bc962335f6e0741154dacdbf8c0c62=1523280957"
}


def valid_name(name):
    reg = re.compile(r'[\\/:*?"<>|\r\n]+')
    valid = reg.findall(name)
    if valid:
        for v in valid:
            name = name.replace(v, '')
    return name


def download(book_id):
    proxies = {'http': 'http://39.134.10.7:8080'}
    url = "http://www.jiaoxueyun.cn/res-view!download.do?resource_id=%s"
    with mysql() as cursor:
        sql = "SELECT * from resource where book_id = '{book_id}' order by chapter_id".format(book_id=book_id)
        cursor.execute(sql)
        data = cursor.fetchall()
    for res in data:
        path = "E:/resource/%s/%s/%s/%s/%s" % (
            res.get('course_name'), res.get('grade_name'), res.get('version_name'), valid_name(res.get('book_name')),
            valid_name(res.get('chapter_name')))
        if not os.path.exists(path):
            os.makedirs(path)
        res_path = "%s/%s.%s" % (path, valid_name(res.get('resource_name')), res.get('type').lower())
        if os.path.exists(res_path):
            continue
        try:
            resp = requests.get(url=url % res.get('resource_id'), headers=head, stream=True,timeout=2)
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
        time.sleep(0.2)


if __name__ == '__main__':
    with mysql() as cursor:
        cursor.execute("SELECT * from book WHERE grade_id in ('G10','G11','G12') and course_name = '英语' limit 10,100")
        book_ids = cursor.fetchall()
    for book in book_ids:
        download(book.get("book_id"))
        # t = threading.Thread(target=download,args=(book.get("book_id"),))
        # t.start()