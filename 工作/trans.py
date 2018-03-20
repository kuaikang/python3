import requests
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


def get_question_ids(cur, chapter_id):
    sql = "SELECT question_id from chapter_question WHERE chapter_id = '%s'"
    cur.execute(sql % chapter_id)
    return cur.fetchall()


def get_question(cur, question_id):
    sql = "SELECT context,type,difficult,answer_url from question WHERE question_id = '%s' and answer_url is not null "
    cur.execute(sql % question_id)
    return cur.fetchall()


def get_tag(cur, tag_id):
    sql = "SELECT tag_name from tag WHERE question_id = '%s'"
    cur.execute(sql % tag_id)
    return cur.fetchone()


def get_item(cur, question_id):
    sql = "SELECT content,`option` from item WHERE question_id = '%s'"
    cur.execute(sql % question_id)
    return cur.fetchall()


def main(currentSubject, importChapterName, import_Chapter, zujuan_chapter):
    db = get_db()
    cur = db.cursor()
    head = {
        "Content-Type": "application/json"
    }
    question_ids = get_question_ids(cur, zujuan_chapter)
    for question_id in question_ids:
        question = get_question(cur, question_id[0])
        for q in question:  # context,type,difficult,answer_url
            req = {"currentSubject": currentSubject, "questionContent": q[0], "importChapterId": import_Chapter,
                   "questionType": "11"}
            tag = get_tag(cur, question_id[0])  # tag[0]
            req["tagUrl"] = tag[0]
            req["importChapterName"] = importChapterName
            req["answerUrl"] = q[3]
            req["difficult"] = q[2]
            items = get_item(cur, question_id[0])
            item = []
            for it in items:  # content,`option`
                item.append({"content": it[0], "option": it[1]})
            req["items"] = item
            requests.post(url="http://localhost:28870/exue-question-system/spark/save", headers=head, json=req)
            time.sleep(0.1)
    cur.close()
    db.close()


if __name__ == '__main__':
    li = [['第1课 人类的形成', '100009001036100001001', '5216'], ['第2课 大河流域', '100009001036100001002', '5217'],
          ['第3课 西方文明之源', '100009001036100001003', '5218'], ['第4课 亚洲封建国家的建立', '100009001036100002001', '5221'],
          ['第5课 中古欧洲社会', '100009001036100002002', '5222'], ['第6课 古代世界的战争与征服', '100009001036100003001', '5224'],
          ['第7课 东西方文化交流的使者', '100009001036100003002', '5225'], ['第8课 古代科技与思想文化(一)', '100009001036100003003', '5226'],
          ['第9课 古代科技与思想文化(二)', '100009001036100003004', '5227'], ['第10课 资本主义时代的曙光', '100009001036100004001', '5229'],
          ['第11课 英国资产阶级革命', '100009001036100004002', '5231'], ['第12课 美国的诞生', '100009001036100004003', '5232'],
          ['第13课 法国大革命和拿破仑帝国', '100009001036100004004', '5233'], ['第14课 “蒸汽时代”的到来', '100009001036100004005', '5235'],
          ['第15课 血腥的资本积累', '100009001036100005001', '5237'], ['第16课 殖民地人民的抗争', '100009001036100005002', '5238'],
          ['第17课 国际工人运动与马克思主义的诞生', '100009001036100006001', '5240'], ['第18课 美国南北战争', '100009001036100006002', '5241'],
          ['第19课 俄国、日本的历史转折', '100009001036100006003', '5242'], ['第20课 人类迈入“电气时代”', '100009001036100007001', '5244'],
          ['第21课 第一次世界大战', '100009001036100007002', '5246'], ['第22课 科学和思想的力量', '100009001036100008001', '5248'],
          ['第23课 世界的文化杰作', '100009001036100008002', '5249']]
    start_time = time.time()
    for i in li:
        print(i)
        main("ls", i[0], i[1], i[2])
    print(time.time() - start_time)
