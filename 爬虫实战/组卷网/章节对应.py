import pymysql
import contextlib


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


def main(res_book_id, zujuan_book_id):
    with mysql(host="123.206.227.74", user="root",
               password="exue2017", db="topic_standard_test", port=3306) as cur_topic:
        sql = "SELECT chapter_name,chapter_id FROM t_res_chapter WHERE book_id = '%s'"
        cur_topic.execute(sql % book_id)
        data = cur_topic.fetchall()
    result = []
    with mysql(host="localhost", user="root",
               password="kuaikang", db="kuaik", port=3333) as cur_zu:
        for d in data:
            sql = "SELECT chapter_id from chapter WHERE book_id = '%s' and chapter_name = '%s'"
            name = d.get('chapter_name').replace(' ', '').replace(' ', '')
            cur_zu.execute(sql % (zujuan_book_id, pymysql.escape_string(name.replace(' ', ''))))
            res = cur_zu.fetchone()
            if res:
                result.append([d.get('chapter_name'), d.get('chapter_id'), res.get('chapter_id')])
            else:
                print(d.get('chapter_name'))
        print(result)
        print(len(result))


if __name__ == '__main__':
    # book_id, zuJuan_book_id = '030003002008040', "77399"  # 英语译林牛津版三下
    # book_id, zuJuan_book_id = '030004002008040', "28459"  # 英语译林牛津版四下
    # book_id, zuJuan_book_id = '030005002008040', "28461"  # 英语译林牛津版五下
    # book_id, zuJuan_book_id = '030006002008040', "28463"  # 英语译林牛津版六下

    # book_id, zuJuan_book_id = '030003002007038', "11424"  # 英语人教版三下（PEP版）
    # book_id, zuJuan_book_id = '030004002007038', "12294"  # 英语人教版四下（PEP版）
    # book_id, zuJuan_book_id = '030005002007038', "12296"  # 英语人教版五下（PEP版）
    # book_id, zuJuan_book_id = '030006002007038', "12298"  # 英语人教版六下（PEP版）

    # book_id, zuJuan_book_id = '030003002009042', "12722"  # 英语外研版三下（三年级起点）
    # book_id, zuJuan_book_id = '030004002009042', "12724"  # 英语外研版四下（三年级起点）
    # book_id, zuJuan_book_id = '030005002009042', "12726"  # 英语外研版五下（三年级起点）
    # book_id, zuJuan_book_id = '030006002009042', "12728"  # 英语外研版六下（三年级起点）

    # book_id, zuJuan_book_id = '030003002017100', "48487"  # 英语冀教版三下（三年级起点）
    # book_id, zuJuan_book_id = '030004002017100', "87436"  # 英语冀教版四下（三年级起点）
    # book_id, zuJuan_book_id = '030005002017100', "48491"  # 英语冀教版五下（三年级起点）
    book_id, zuJuan_book_id = '030006002017100', "48493"  # 英语冀教版六下（三年级起点）
    main(book_id, zuJuan_book_id)
