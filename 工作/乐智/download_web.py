from selenium import webdriver
import pymysql
import contextlib
import time

# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='localhost', port=3306, user='root', password='123456', db='lezhi', charset='utf8'):
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
    download_url = "http://www.jiaoxueyun.cn/res-view!download.do?resource_id={resource_id}"
    driver = webdriver.Chrome()
    input(">>:")
    with mysql() as cur:
        cur.execute("SELECT * from book WHERE grade_id < 'G10' and course_name = '语文' LIMIT 10;")
        for book in cur.fetchall():
            cur.execute("SELECT * FROM `resource` WHERE book_id = %s;"%book.get('book_id'))
            for res in cur.fetchall():
                time.sleep(0.8)
                driver.get(download_url.format(resource_id=res.get('resource_id')))
    driver.quit()
