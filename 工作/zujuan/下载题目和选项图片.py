import pymysql
import requests
import re
import os
import threading


def get_db_sit():
    # 打开数据库连接
    try:
        db = pymysql.connect(
            host="123.206.227.74", user="root",
            password="exue2017", db="sit_exue_resource", port=3306,
            charset="utf8"
        )
        return db
    except Exception as e:
        print(e)


def download(subject_key, urls):
    with requests.session() as session:
        for u in urls:
            response = session.get(u)
            if response.status_code != 200:
                print("failed", u)
            arr = u.split('/')
            path = "E:/question/{subject_key}/{first}/{second}".format(subject_key=subject_key, first=arr[-3],
                                                                       second=arr[-2])
            if not os.path.exists(path):
                os.makedirs(path)  # 假如路径不存在则创建
            f = open("{path}/{file_name}".format(path=path, file_name=arr[-1]), mode="wb")
            f.write(response.content)
            f.close()


def get_urls(subject_key):
    db = get_db_sit()
    cursor = db.cursor()
    cursor.execute(
        "SELECT content from t_res_{subject_key}_item WHERE content like '%src%' and create_time > '2018-03-01'".format(
            subject_key=subject_key))
    urls = cursor.fetchall()
    data = set()
    pattern = re.compile('.*?src="(.*?)"', re.S)
    print(len(urls))
    for u in urls:
        src = re.findall(pattern, u[0])
        for item in src:
            t = item[-3:]
            if 'png' == t or 'jpg' == t or 'gif' == t:
                data.add(item)
    print(len(data))
    res = list(data)
    for i in range(40):
        count = len(res) // 40 + 1
        t = threading.Thread(target=download, args=(subject_key, res[i * count:(i + 1) * count]))
        t.start()


if __name__ == '__main__':
    get_urls('sx')
    # sx yw ls wl yy hx dl sw