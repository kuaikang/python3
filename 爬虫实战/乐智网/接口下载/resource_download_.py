import requests
import pymysql
import os
import re
import time
import contextlib
import queue
import threading


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
    "Cookie": "UM_distinctid=162467338a7c60-0a686962135185-3a61430c-1fa400-162467338a826e; remPassord_=true; userName=13965127823; userPassword=yj65127823; remPassord=true; loginName=13965127823; loginPwd=yj65127823; name=value; goa_page_pagesize_gotoPage=12; JSESSIONID=8279553F4B33F2A6A0A985097B38E833; CNZZDATA1253279410=1838872367-1523255924-http%253A%252F%252Fwww.jiaoxueyun.cn%252F%7C1524017100; Hm_lvt_3b2b90b968014bee5b24ff51962ad7ac=1523256735,1523959116,1524017533; Hm_lvt_83bc962335f6e0741154dacdbf8c0c62=1523256735,1523959116,1524017533; JYY-Cookie-20480=EELHKIMAFAAA; Hm_lpvt_83bc962335f6e0741154dacdbf8c0c62=1524021842; Hm_lpvt_3b2b90b968014bee5b24ff51962ad7ac=1524021842"
}


def valid_name(name):
    reg = re.compile(r'[\\/:*?"<>|\r\n]+')
    valid = reg.findall(name)
    if valid:
        for v in valid:
            name = name.replace(v, '')
    return name


resource_queue = queue.Queue()  # 存放下载的资源id


def download(book_id):
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
            resp = requests.get(url=url % res.get('resource_id'), headers=head, stream=True, timeout=2)
        except Exception:
            continue
        if '登录' not in resp.text or "资" not in resp.text:
            print(res_path)
            f = open(res_path, mode="wb")
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
            f.close()
            resource_queue.put(res.get('resource_id'))
            print("put", res.get('resource_id'))
        resp.close()
        time.sleep(0.3)


def main(data):
    for d in data:
        download(d)


def remove():
    while True:
        if resource_queue.empty(): continue
        resource_id = resource_queue.get(False)
        print(resource_id)
        print("get", resource_id)
        resp = requests.post("http://www.jiaoxueyun.cn/personal!deleteDownload.do", data={"key": resource_id}, headers=head)
        print(resp.status_code)


if __name__ == '__main__':
    book_ids = ['3736', 'ff8080814467cea80144681413c7027c', 'ff8080814467cea8014468172fd1029c',
                'ff8080814467cea80144681f50c70300', 'ff8080814467cea80144683d582603e6',
                'ff8080814467cea8014468404ea00407', '3528', '3607', '3739', 'ff8080814467cea80144680c079d0251',
                'ff8080814467cea801446826ceb1034a', 'ff8080814467cea80144682d1f9a0375']
    t = threading.Thread(target=main, args=(book_ids,))
    t.start()
    t1 = threading.Thread(target=remove, args=())
    t1.start()
