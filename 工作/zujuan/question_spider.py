import requests
from urllib.parse import urlencode
import pymysql, time
from selenium import webdriver
import contextlib


# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='localhost', port=3333, user='root', password='kuaikang', db='kuaik', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    finally:
        conn.commit()
        cur.close()
        conn.close()


driver = webdriver.Chrome()


def get_question_url(categories, page):
    url = "http://www.zujuan.com/question/list?"
    req = {
        "categories": categories,
        "question_channel_type": "1",  # 题型
        "difficult_index": "",
        "grade_id[]": "0",
        "page": page,
        "kid_num": "",
        "exam_type": "",
        "sortField": "time",
        "_": "1523323489804"
    }
    data = []
    for i in range(3):
        data.append({"grade_id[]": str(i + 7)})
    url += urlencode(req)
    for d in data:
        url += "&" + urlencode(d)
    return url


def parse_data(url):
    driver.get(url)
    print(driver.page_source)
    input(">>:")


def main(subject_key, book_id):
    sql_chap = "SELECT chapter_id from chapter WHERE book_id = '{book_id}'".format(book_id=book_id)
    sql_q = "INSERT INTO yw_question (`question_id`, `context`, `type`, `difficult`) VALUES ('{0}', '{1}', '{2}', '{3}')"
    sql_cq = 'INSERT INTO yw_chapter_question (`id`,`chapter_id`, `question_id`) VALUES (UUID(),"{0}", "{1}");'
    sql_t = 'INSERT INTO yw_tag (`tag_id`, `tag_name`, `question_id`) VALUES (UUID(), "{0}", "{1}");'
    with mysql() as cur:
        cur.execute(sql_chap)
        chapter_ids = cur.fetchall()
        print(chapter_ids)
        for line in chapter_ids:
            for i in range(1, 100):
                data, total = get_question(line[0], i)
                if not data: break
                page = (total + 10 - 1) // 10
                print(line[0], page, i)
                if i > page: break
                for js in data:
                    quest = js.get("questions")
                    for q in quest:
                        if isinstance(q.get("options"), str):
                            continue
                        if isinstance(q.get("options"), list):
                            continue
                        try:
                            cur.execute(sql_cq.format(line[0], q.get("question_id")))
                            cur.execute(
                                "SELECT * FROM yw_question WHERE question_id = '%s'" % q.get("question_id"))
                            if not cur.fetchone():
                                cur.execute(
                                    sql_q.format(q.get("question_id"), pymysql.escape_string(q.get("question_text")),
                                                 q.get("question_type"),
                                                 q.get("difficult_index")))
                                for key in q.get("options").keys():
                                    sql_i = 'INSERT INTO yw_item (`item_id`, `content`, `option`,`question_id`) VALUES (UUID(), "{0}", "{1}","{2}");'
                                    cur.execute(sql_i.format(pymysql.escape_string(q.get("options").get(key)), key,
                                                             q.get("question_id")))
                                cur.execute(sql_t.format(q.get("knowledge"), q.get("question_id")))
                        except Exception as e:
                            print(e)
                            continue
                    time.sleep(0.2)


if __name__ == '__main__':
    input(">>:")
    main("ls", "120778")
    driver.quit()

# print(q.get("question_text"))
# print(q.get("options"))  # 选项
# print(q.get("knowledge"))  # 知识点
# print(q.get("question_id"))  # 问题id
# print(q.get("question_type"))  # 问题类型 1单选 2多选 3判断 4填空 6解答 26实验综合题 28综合题
# print(q.get("difficult_index"))  # 难度 1.容易 3.普通 5.困难
