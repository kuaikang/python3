import pymysql
import re
from aiohttp import ClientSession
import asyncio
import os
import time


def get_db_spark():
    # 打开数据库连接
    try:
        db = pymysql.connect(
            host="123.206.227.74", user="root",
            password="exue2017", db="zujuan_spark_test", port=3306,
            charset="utf8"
        )
        return db
    except Exception as e:
        print(e)


async def download(data, subject_key):
    pattern = re.compile('.*?src="(.*?)"', re.S)
    async with ClientSession() as session:
        for d in data:
            if 'src' not in d[0]: continue
            s = re.findall(pattern, d[0])
            for index, item in enumerate(s):
                if len(s) == 2 and s[0] == s[1] and index == 1:
                    continue
                if 'png' in item or 'jpg' in item or 'gif' in item:
                    print(item, subject_key)
                    try:
                        async with session.get(item, timeout=20) as response:
                            response = await response.read()
                            path = 'E:/question/%s/%s/%s' % (subject_key, item.split('/')[-3], item.split('/')[-2])
                            if not os.path.exists(path):
                                os.makedirs(path)
                            f = open('%s/%s' % (path, item.split('/')[-1]), mode="wb")
                            f.write(response)
                            f.close()
                            response.close()
                            time.sleep(0.3)
                    except Exception:
                        print()


def main(subject_key):
    db = get_db_spark()
    cur = db.cursor()
    data = []
    sql = "select content from t_res_{subject_key}_item WHERE content like '%src%' limit {index},{count}"
    for i in range(20):
        cur.execute(sql.format(subject_key=subject_key, index=i * 2050, count=2050))
        data.append(cur.fetchall())
    cur.close()
    db.close()
    tasks = []
    for d in data:
        task = asyncio.ensure_future(download(d, subject_key))
        tasks.append(task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    main("sx")
