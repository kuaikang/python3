import requests, json, re, threading
from bs4 import BeautifulSoup
from 数据库存储.Mysql import pymysql_util
import time

cz_dic = {"2": "语文", "3": "数学", "4": "英语", "6": "物理", "7": "化学", "8": "历史", "9": "政治思品", "10": "地理", "11": "生物"}


# 获取出版版本
def get_version(xd, channel):
    resp = requests.get("http://tiku.21cnjy.com/tiku.php?mod=quest&channel=%s&xd=%s" % (channel, xd))
    soup = BeautifulSoup(resp.text, "lxml")
    data = soup.find_all(attrs={"class": "hasChildren"})
    result = []
    for item in data:  # item["id"] 版本id  item.get_text().strip() 版本名 item.select("a")[0]["href"] 路径
        it = [cz_dic[channel], channel, item.get_text().strip(), item["id"]]
        result.append(it)
    return result


# 获取书本
def get_book(version_id):
    req = {"root": version_id, "op": "ajaxcatid", "additional": "yeah: Tue, 13 Mar 2018 15:21:17 GMT"}
    resp = requests.post(url="http://tiku.21cnjy.com/tiku.php?mod=quest", data=req)
    if len(resp.json()) == 0:
        return None
    pattern_book = re.compile('.*?catid=(\d+)">(.*?)<.*?', re.S)
    result = []
    for it in resp.json():
        d = re.findall(pattern_book, it.get("text"))
        result.append(d[0])
    return result


def get_unit(book_id):
    units = get_book(book_id[0])
    if units:
        count = 1
        sql = 'INSERT INTO unit (unit_id, unit_name, book_id, num) VALUES ("%s", "%s", "%s", %s)'
        data = []
        for unit in units:  # ('22783', '第一单元 成长的足迹')
            u = [unit[0], unit[1], book_id[0], count]
            data.append(u)
            count += 1
        pymysql_util.insert_many(db, sql, data=data)
        time.sleep(1)


if __name__ == '__main__':
    db = pymysql_util.get_db()
    # for s in cz_dic.keys():
    #     versions = get_version(xd='2', channel=s)
    #     for item in versions:  # ['语文', '2', '北师大版', '10426']
    #         # pymysql_util.insert_one(db, "INSERT INTO editor (edition_id, edition_name) VALUES ('%s','%s')" % (
    #         #     str(item[3]), item[2]))
    #         books = get_book(item[-1])
    #         for book in books:  # '1436','七年级上册（2016）'
    #             # sql = "INSERT INTO book (book_id, book_name, grade_id, edition_id, edition_name) VALUES ('%s', '%s', '%s', '%s', '%s')"
    #             # pymysql_util.insert_one(db, sql % (book[0], book[1], '2', item[3], item[2]))
    #             units = get_book(book[0])
    #             if units:
    #                 count = 1
    #                 for unit in units:  # ('22783', '第一单元 成长的足迹')
    #                     sql = "INSERT INTO unit (unit_id, unit_name, book_id, num) VALUES ('%s', '%s', '%s', %s)"
    #                     pymysql_util.insert_one(db, sql % (unit[0], unit[1], book[0], count))
    #                     count += 1
    #                     # chapters = get_book(unit[0])
    #                     # if chapters:
    #                     #     print(chapters)

    books = pymysql_util.find_all(db, "select book_id from book")
    for book_id in books:
        t = threading.Thread(target=get_unit, args=(book_id,))
        t.start()
