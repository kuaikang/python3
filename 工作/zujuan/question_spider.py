import requests
from urllib.parse import urlencode
import pymysql, time


def get_db():
    # 打开数据库连接
    try:
        db = pymysql.connect(
            host="localhost", user="root",
            password="kuaikang", db="kuaik", port=3333,
            charset="utf8"
        )
        return db
    except Exception as e:
        print(e)


def get_question(categories, page):
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
        "_": "1521515844117"
    }
    grade7 = {"grade_id[]": "7"}
    grade8 = {"grade_id[]": "8"}
    grade9 = {"grade_id[]": "9"}
    head = {
        "Cookie":"isRemove=1; _ga=GA1.2.1209185538.1520329414; _gid=GA1.2.1039098456.1521423702; PHPSESSID=o48ef3voq3mp2ddvmm4r9sn0m2; _csrf=5664bfe3243bfe468a51427ec4cd2ec4650a84479b67bc1da467c20f95ee2fcfa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22a31fbBxiN-82_bb9poobIoQpJTaPMwJf%22%3B%7D; isRemove=1; xd=302c76d9e27c6fb0e1f815bdf637ae7f9ec27997dd7c18c9fcf7c68da09ff5c8a%3A2%3A%7Bi%3A0%3Bs%3A2%3A%22xd%22%3Bi%3A1%3Bs%3A1%3A%222%22%3B%7D; Hm_lvt_6de0a5b2c05e49d1c850edca0c13051f=1521680386,1521683439,1521715177,1521786389; chid=753411127a26c0bf4f88c5bb0c64e771512616316bae9de43cb9a9038d6b13ffa%3A2%3A%7Bi%3A0%3Bs%3A4%3A%22chid%22%3Bi%3A1%3Bs%3A1%3A%223%22%3B%7D; _gat_gtag_UA_112991577_1=1; Hm_lpvt_6de0a5b2c05e49d1c850edca0c13051f=1521786832",
        "X-CSRF-Token": "YuvZ0usGfrQHZJ9QxC4RghO0y-1dTrxnimhxKsm4w6QA0piqo3FJ-kUoxTyTY33JUOWOvTIK6gnOLygTpIyb1g==",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
    }
    params = urlencode(req) + "&" + urlencode(grade7) + "&" + urlencode(grade8) + "&" + urlencode(grade9)
    resp = requests.get(url + params, headers=head)
    resp.close()
    return resp.json().get("data"), resp.json().get("total")


def main(book_id):
    db = get_db()
    cur = db.cursor()
    sql_chap = "SELECT chapter_id from chapter WHERE book_id = '%s'" % book_id
    cur.execute(sql_chap)
    chapter_ids = cur.fetchall()
    print(chapter_ids)
    sql_q = "INSERT INTO `kuaik`.`question` (`question_id`, `context`, `type`, `difficult`) VALUES ('{0}', '{1}', '{2}', '{3}')"
    sql_cq = 'INSERT INTO `kuaik`.`chapter_question` (`id`,`chapter_id`, `question_id`) VALUES (UUID(),"{0}", "{1}");'
    sql_t = 'INSERT INTO `kuaik`.`tag` (`tag_id`, `tag_name`, `question_id`) VALUES (UUID(), "{0}", "{1}");'
    for line in chapter_ids:
        for i in range(1, 100):
            if i == 15:break
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
                            "SELECT * FROM `kuaik`.`question` WHERE question_id = '%s'" % q.get("question_id"))
                        if not cur.fetchone():
                            cur.execute(
                                sql_q.format(q.get("question_id"), pymysql.escape_string(q.get("question_text")),
                                             q.get("question_type"),
                                             q.get("difficult_index")))
                            for key in q.get("options").keys():
                                sql_i = 'INSERT INTO `kuaik`.`item` (`item_id`, `content`, `option`,`question_id`) VALUES (UUID(), "{0}", "{1}","{2}");'
                                cur.execute(sql_i.format(pymysql.escape_string(q.get("options").get(key)), key,
                                                         q.get("question_id")))
                            cur.execute(sql_t.format(q.get("knowledge"), q.get("question_id")))
                    except Exception as e:
                        print(e)
                        continue
                db.commit()
                time.sleep(0.1)
    cur.close()
    db.close()


if __name__ == '__main__':
    main("11420")

# print(q.get("question_text"))
# print(q.get("options"))  # 选项
# print(q.get("knowledge"))  # 知识点
# print(q.get("question_id"))  # 问题id
# print(q.get("question_type"))  # 问题类型 1单选 2多选 3判断 4填空 6解答 26实验综合题 28综合题
# print(q.get("difficult_index"))  # 难度 1.容易 3.普通 5.困难
