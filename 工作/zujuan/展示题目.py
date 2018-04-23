import pymysql
import contextlib
import re


@contextlib.contextmanager
def mysql(host='123.206.227.74', port=3306, user='root', password='exue2017', db='sit_exue_resource', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    finally:
        conn.commit()
        cur.close()
        conn.close()


if __name__ == '__main__':
    with mysql() as cur:
        cur.execute("SELECT * from t_res_wl_item WHERE content like '%dfs.view-res.jzexueyun.com/q%' and create_time > '2018-04-16';")
        data = cur.fetchall()
        pattern = re.compile("<img.*?>",re.S)
        f = open("F:/wl_item.html",mode="a",encoding="utf8")
        for d in data:
            src = re.findall(pattern,d.get('content'))
            f.write(d.get('question_uuid'))
            for s in src:
                f.write(s)
            f.write("</br>")
        f.close()