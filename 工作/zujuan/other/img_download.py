import requests
import pymysql, threading, time


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


# 下载知识点图片
def img_download(index):
    select_tag = "SELECT tag_id,tag_name,question_id FROM `tag` limit %s,100" % index
    db = get_db()
    cur = db.cursor()
    cur.execute(select_tag)
    tags = cur.fetchall()
    cur.close()
    db.close()
    for tag in tags:
        resp = requests.get(tag[1])
        f = open("../img/%s.png" % tag[0], mode="wb")
        f.write(resp.content)
        f.close()
        resp.close()


if __name__ == '__main__':
    for i in range(50):
        t = threading.Thread(target=img_download, args=(i * 100,))
        t.start()
