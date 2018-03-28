import pymysql
import re
import requests
import os


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


def main(subject_key):
    sql = 'select uuid,context from t_res_%s_question' % subject_key
    sql_update_url = "UPDATE t_res_{subject_key}_question SET context = replace(context,'{old_url}','{new_url}') WHERE uuid = '{uuid}'"
    db = get_db_spark()
    cur = db.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    pattern = re.compile('.*?src="(.*?)"', re.S)
    for d in data:
        if 'src' not in d[1]: continue
        s = re.findall(pattern, d[1])
        for index, item in enumerate(s):
            if len(s) == 2 and s[0] == s[1] and index == 1:
                continue
            if 'png' in item or 'jpg' in item:
                print(item)
                resp = requests.get(item)
                path = 'E:/question/%s/%s/%s' % (subject_key, item.split('/')[-3], item.split('/')[-2])
                if not os.path.exists(path):
                    os.makedirs(path)
                f = open('%s/%s' % (path, item.split('/')[-1]), mode="wb")
                f.write(resp.content)
                f.close()
                resp.close()
                # 上传图片
                f_new = open('%s/%s' % (path, item.split('/')[-1]), mode="rb")
                files = {'file': [item.split('/')[-1], f_new, 'application/octet-stream']}
                response = requests.post(url='http://dfs.upload1.jzexueyun.com/cos/upload', files=files)
                new_url = response.json().get('content').get('accessUrl')
                print(new_url)
                response.close()
                cur.execute(sql_update_url.format(subject_key=subject_key, old_url=item, new_url=new_url, uuid=d[0]))
                f_new.close()
            db.commit()
    cur.close()
    db.close()


if __name__ == '__main__':
    # main('dl')
    db = get_db_spark()
    cur = db.cursor()
    cur.execute('select uuid,context from t_res_dl_question')
    data = cur.fetchall()
    pattern = re.compile('.*?src="(.*?)"', re.S)
    for d in data:
        if 'src' in d[1]:
            print(re.findall(pattern,d[1]))