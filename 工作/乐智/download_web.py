from selenium import webdriver
import pymysql
import contextlib
import time


# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='localhost', port=3333, user='root', password='kuaikang', db='lezhi', charset='utf8'):
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
        book_ids = ['ff8080814486454301449b3f05ad0871', 'ff8080814486454301449b4953e90890']
        for book_id in book_ids:
            cur.execute("SELECT * FROM `resource` WHERE book_id = '{book_id}';".format(book_id=book_id))
            for res in cur.fetchall():
                time.sleep(0.6)
                driver.get(download_url.format(resource_id=res.get('resource_id')))
    driver.quit()
