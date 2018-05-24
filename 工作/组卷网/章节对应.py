import pymysql
import contextlib
from common.string_util import get_similarity


# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='localhost', port=3333, user='root', password='kuaikang', db='kuaik', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)
    conn.autocommit(True)
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    finally:
        conn.commit()
        cur.close()
        conn.close()


def valid_name(name):
    useless = "、（）().\r\n——"
    for u in useless:
        name = name.replace(u, '')
    return name


def main(res_book_id, zujuan_book_id):
    with mysql(host="123.206.227.74", user="root",
               password="exue2017", db="topic_standard_test", port=3306) as cur_topic:
        sql = "SELECT chapter_name,chapter_id FROM t_res_chapter WHERE book_id = '{res_book_id}'"
        cur_topic.execute(sql.format(res_book_id=res_book_id))
        data1 = cur_topic.fetchall()
    with mysql(host="localhost", user="root",
               password="kuaikang", db="kuaik", port=3333) as cur_zu:
        sql = "SELECT * from chapter WHERE book_id = '{zujuan_book_id}'"
        cur_zu.execute(sql.format(zujuan_book_id=zujuan_book_id))
        data2 = cur_zu.fetchall()
    result = []
    for data in data1:
        flag = True
        for item in data2:
            if get_similarity(valid_name(data.get('chapter_name')), valid_name(item.get('zj_chapter_name'))) > 0.7:
                result.append([data.get('chapter_name'), data.get('chapter_id'), item.get('zj_chapter_id'),
                               item.get('zj_chapter_name')])
                flag = False
        if flag:
            print(data.get('chapter_name'))
    return result


def update_chapter(data):
    sql = "update chapter set chapter_id = '{0}',chapter_name='{1}' WHERE zj_chapter_id = {2};"
    for d in data:
        print(sql.format(d[1], pymysql.escape_string(d[0]), d[2]))


if __name__ == '__main__':
    data = [
        ['020007001139100', '25388'],
        ['020007002139100', '26821'],
        ['020008001139100', '26822'],
    ]
    result = []
    for data in data:
        print(data)
        res = main(data[0], data[1])
        print(res)
        for r in res:
            result.append(r)
    print(result)
    print(len(result))
    print("\n\n")
    update_chapter(result)
