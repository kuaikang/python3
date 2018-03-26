import requests
import pymysql
import os
import threading


def get_db():
    # 打开数据库连接
    try:
        db = pymysql.connect(
            host="localhost", user="root",
            password="123456", db="lezhi", port=3306,
            charset="utf8"
        )
        return db
    except Exception as e:
        print(e)


head = {
    "Cookie":"UM_distinctid=1624e0ec632182-0c324f9f49603f-3a61430c-100200-1624e0ec6354af; name=value; goa_page_pagesize_gotoPage=12; remPassord_=true; userName=13965127823; userPassword=yj65127823; wP_h=716e702abcf2ca100644575e712c0d5214902c22; JSESSIONID=96995A5C44BFAA34F53C3BEFBDBC27AC; JYY-Cookie-20480=EGLHKIMAFAAA; Hm_lvt_3b2b90b968014bee5b24ff51962ad7ac=1521737307,1521812600,1521884458,1521937934; Hm_lvt_83bc962335f6e0741154dacdbf8c0c62=1521737307,1521812600,1521884458,1521937934; remPassord=true; loginName=13965127823; loginPwd=yj65127823; CNZZDATA1253279410=1856900147-1521726488-http%253A%252F%252Fwww.jiaoxueyun.cn%252F%7C1521934916; Hm_lpvt_83bc962335f6e0741154dacdbf8c0c62=1521938002; Hm_lpvt_3b2b90b968014bee5b24ff51962ad7ac=1521938002"
}


def download(book_id):
    url = "http://www.jiaoxueyun.cn/res-view!download.do?resource_id=%s"
    db = get_db()
    cur = db.cursor()
    sql = "SELECT b.course_name,b.grade_name,b.book_name,c.chapter_name,r.resource_id,r.resource_name, r.type, " \
          "b.version_name FROM resource r LEFT JOIN chapter c ON r.chapter_id = c.chapter_id LEFT JOIN book b " \
          "on r.book_id = b.book_id WHERE r.book_id = '%s' and c.lesson_type != '0'" % book_id
    cur.execute(sql)
    data = cur.fetchall()
    for res in data:
        path = "E:/resource/%s/%s/%s/%s/%s" % (res[0], res[1], res[7], res[2].replace("?", ""), res[3].replace("?", ""))
        if not os.path.exists(path):
            os.makedirs(path)
        if os.path.exists("%s/%s.%s" % (path, res[5].replace("?", ""), res[6].lower())):
            continue
        try:
            resp = requests.get(url=url % res[4], headers=head, stream=True)
        except Exception:
            continue
        if '登录' not in resp.text:
            print("%s/%s.%s" % (path, res[5].replace("?", ""), res[6].lower()))
            f = open("%s/%s.%s" % (path, res[5].replace("?", ""), res[6].lower()), mode="wb")
            for chunk in resp.iter_content(chunk_size=2048):
                if chunk:
                    f.write(chunk)
            f.close()
        resp.close()
    cur.close()
    db.close()


if __name__ == '__main__':
    book_ids = ["3201", "3985"]
    for book_id in book_ids:
        download(book_id)
