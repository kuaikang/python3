import requests
from urllib.parse import urlencode
import pymysql, time


def get_db():
    # 打开数据库连接
    try:
        db = pymysql.connect(
            host="192.168.121.40", user="root",
            password="001233", db="kuaik", port=3306,
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
        "_": "1521278650387"
    }
    grade7 = {"grade_id[]": "7"}
    grade8 = {"grade_id[]": "8"}
    grade9 = {"grade_id[]": "9"}
    head = {
        "Cookie": "_ga=GA1.2.1209185538.1520329414; device=310bdaba05b30bb632f66fde9bf3e2b91ebc4d607c250c2e1a1d9e0dfb900f01a%3A2%3A%7Bi%3A0%3Bs%3A6%3A%22device%22%3Bi%3A1%3BN%3B%7D; PHPSESSID=gsmlfat1tolqaisv64asrtsad6; xd=75519cb9f2bf90d001c0560f5c40520062a60ada9cb38350078f83e04ee38a31a%3A2%3A%7Bi%3A0%3Bs%3A2%3A%22xd%22%3Bi%3A1%3Bi%3A2%3B%7D; _csrf=75b3998320bbf62cb8c735d01eb7311c1174b698213564ba79af1ff1753cf915a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22ivfHrmDlJhZ1kkm37njpwLdCWTvHbEI_%22%3B%7D; _gid=GA1.2.1039098456.1521423702; _gat_gtag_UA_112991577_1=1; isRemove=1; Hm_lvt_6de0a5b2c05e49d1c850edca0c13051f=1521170767,1521177189,1521423696,1521423702; chid=73f77ea0c6d8f078f9adfd8acef66fa3c01401d5245f373d4707a757cca2d8bea%3A2%3A%7Bi%3A0%3Bs%3A4%3A%22chid%22%3Bi%3A1%3Bs%3A1%3A%228%22%3B%7D; Hm_lpvt_6de0a5b2c05e49d1c850edca0c13051f=1521423729",
        "X-CSRF-Token": "FKEzaBYESs_9_nKoWTzusTm84t9AYnZGppDHWpGTsLt911UgZGkOo7eWKJkyV4OCDtKIrzcuEgXxxLES89b55A==",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
    }
    params = urlencode(req) + "&" + urlencode(grade7) + "&" + urlencode(grade8) + "&" + urlencode(grade9)
    resp = requests.get(url + params, headers=head)
    resp.close()
    return resp.json().get("data"), resp.json().get("total")
    # for js in resp.json().get("data"):
    #     quest = js.get("questions")
    #     for q in quest:
    #         print(q.get("question_text"))
    #         print(q.get("options"))  # 选项
    #         print(q.get("knowledge"))  # 知识点
    #         print(q.get("question_id"))  # 问题id
    #         print(q.get("question_type"))  # 问题类型 1单选 2多选 3判断 4填空 6解答 26实验综合题 28综合题
    #         print(q.get("difficult_index"))  # 难度 1.容易 3.普通 5.困难


def main():
    db = get_db()
    cur = db.cursor()
    sql_chap = "SELECT c.chapter_id from chapter c LEFT JOIN chapter_question qc " \
               "on c.chapter_id = qc.chapter_id WHERE qc.question_id is null and c.chapter_id in " \
               "(SELECT chapter_id from chapter ch LEFT JOIN book b on ch.book_id = b.book_id " \
               "WHERE b.subject_id = '8' and b.period = '2') limit 100"
    cur.execute(sql_chap)
    chapter_ids = cur.fetchall()
    print(chapter_ids)
    for line in chapter_ids:
        # f = open("cz_chapter.txt",mode="r",encoding="utf8")
        # for line in f.readlines()[301:600]:
        #     line = line.split(",")
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
                    sql_q = "INSERT INTO `kuaik`.`question` (`question_id`, `context`, `type`, `difficult`) VALUES ('{0}', '{1}', '{2}', '{3}')"
                    sql_cq = 'INSERT INTO `kuaik`.`chapter_question` (`id`,`chapter_id`, `question_id`) VALUES (UUID(),"{0}", "{1}");'
                    sql_t = 'INSERT INTO `kuaik`.`tag` (`tag_id`, `tag_name`, `question_id`) VALUES (UUID(), "{0}", "{1}");'
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
                        db.commit()
                    except Exception as e:
                        print(e)
    cur.close()
    db.close()


if __name__ == '__main__':
    for i in range(9):
        main()
        time.sleep(60)

# print(q.get("question_text"))
# print(q.get("options"))  # 选项
# print(q.get("knowledge"))  # 知识点
# print(q.get("question_id"))  # 问题id
# print(q.get("question_type"))  # 问题类型 1单选 2多选 3判断 4填空 6解答 26实验综合题 28综合题
# print(q.get("difficult_index"))  # 难度 1.容易 3.普通 5.困难
