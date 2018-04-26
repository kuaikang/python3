import contextlib
import pymysql


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


if __name__ == '__main__':
    sql = "update wl_tag_question set tag_id = '{tag_id}' WHERE question_uuid = '{question_uuid}'"
    tag_id = 30000000
    with mysql() as cur:
        cur.execute("select * from wl_tag_question")
        for item in cur.fetchall():
            cur.execute(sql.format(tag_id=tag_id,question_uuid=item.get('question_uuid')))
            tag_id += 1