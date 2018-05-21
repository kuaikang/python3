from urllib.parse import urlencode
import json
import time
from selenium import webdriver
from common.mongo_util import mongo_operate
from common.mysql_util import mysql


def get_chapter_id(book_id):
    with mysql(host='localhost', port=3333, user='root', password='kuaikang', db='kuaik') as cur:
        select_chapter_sql = "SELECT * from chapter WHERE book_id = '{}'".format(book_id)
        cur.execute(select_chapter_sql)
        data = cur.fetchall()
        return [item.get('zj_chapter_id') for item in data]


def get_request_url(categories, page):
    url = "http://www.zujuan.com/question/list?"
    req = {
        "categories": categories,
        "page": page,
        "question_channel_type": "1",  # 题型
        "difficult_index": "",
        "grade_id[]": "0",
        "kid_num": "",
        "exam_type": "",
        "sortField": "time",
        "_": "1521515844117"
    }
    data = []
    url += urlencode(req)
    for i in range(6):
        data.append({"grade_id[]": str(i + 1)})
    url += urlencode(req)
    for d in data:
        url += "&" + urlencode(d)
    return url


driver = webdriver.Chrome()


def parse_data(categories, page):
    url = get_request_url(categories, page)
    driver.get(url)
    time.sleep(2)
    s = driver.find_element_by_tag_name("pre").text
    data = json.loads(s)
    if not data.get('data'):
        return None, None
    return data.get("data")[0].get("questions"), (data.get("total") + 10 - 1) // 10


def main(subject_key, book_id):
    for c_id in get_chapter_id(book_id):
        for page in range(1, 31):
            questions, total_page = parse_data(c_id, page)
            print(c_id, total_page, page)
            if total_page < page: break
            if not questions: break
            for q in questions:
                op.insert(q)


op = mongo_operate()

if __name__ == '__main__':
    input(">>:")
    sx = ['25572', '25573']
    for item in sx:
        main("sx", item)
    driver.quit()
    op.release()
