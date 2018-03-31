import pymysql
import re
from aiohttp import ClientSession
import asyncio
import os
import time


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


def valid_name(name):
    reg = re.compile(r'[\\/:*?"<>|\r\n]+')
    valid = reg.findall(name)
    if valid:
        for v in valid:
            name = name.replace(v, '')
    return name


head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    "Cookie": "UM_distinctid=1624e0ec632182-0c324f9f49603f-3a61430c-100200-1624e0ec6354af; remPassord_=true; userName=13965127823; userPassword=yj65127823; remPassord=true; loginName=13965127823; loginPwd=yj65127823; wP_h=716e702abcf2ca100644575e712c0d5214902c22; name=value; goa_page_pagesize_gotoPage=12; JSESSIONID=72A1309E6D1EB32EA3C09F064A93F59F; JYY-Cookie-20480=EFLHKIMAFAAA; Hm_lvt_83bc962335f6e0741154dacdbf8c0c62=1522069899,1522334103,1522334113,1522505080; Hm_lvt_3b2b90b968014bee5b24ff51962ad7ac=1522069899,1522334103,1522334113,1522505080; CNZZDATA1253279410=1856900147-1521726488-http%253A%252F%252Fwww.jiaoxueyun.cn%252F%7C1522500177; Hm_lpvt_83bc962335f6e0741154dacdbf8c0c62=1522505095; Hm_lpvt_3b2b90b968014bee5b24ff51962ad7ac=1522505095"
}

url = "http://www.jiaoxueyun.cn/res-view!download.do?resource_id={resource_id}"


async def download(data):
    async with ClientSession() as session:
        for res in data:
            resource_name = valid_name(res[5])
            r_type = res[6].lower()
            path = "E:/resource/{subject}/{grade}/{version}/{book_name}/{chapter_name}".format(
                subject=res[0], grade=res[1], version=res[7], book_name=valid_name(res[2]),
                chapter_name=valid_name(res[3]))
            if not os.path.exists(path):
                os.makedirs(path)
            resource_url = path + '/' + resource_name + '.' + r_type  # 资源路径
            if os.path.exists(resource_url):  # 判断是否已下载过该资源
                continue
            async with session.get(url.format(resource_id=res[4]), headers=head) as response:
                response = await response.read()
                f = open(resource_url, mode="wb")
                f.write(response)
                f.close()
                print(resource_url)
                time.sleep(0.4)


def main():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT book_id FROM book WHERE grade_id in ('G10','G11','G12') ORDER BY book_id LIMIT 0,3")
    sql = "SELECT b.course_name,b.grade_name,b.book_name,c.chapter_name,r.resource_id,r.resource_name, r.type, " \
          "b.version_name FROM resource r LEFT JOIN chapter c ON r.chapter_id = c.chapter_id LEFT JOIN book b " \
          "on r.book_id = b.book_id WHERE r.book_id = '{book_id}'"
    book_ids = cur.fetchall()
    data = []
    for b in book_ids:
        cur.execute(sql.format(book_id=b[0]))
        data.append(cur.fetchall())
    cur.close()
    db.close()
    tasks = []
    for d in data:
        task = asyncio.ensure_future(download(d))
        tasks.append(task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    main()
