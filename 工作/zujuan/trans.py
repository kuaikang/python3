import requests
import pymysql, time, threading


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


def get_question_ids(cur, chapter_id):
    sql = "SELECT question_id from chapter_question WHERE chapter_id = '%s'"
    cur.execute(sql % chapter_id)
    return cur.fetchall()


def get_question(cur, question_id):
    sql = "SELECT context,type,difficult,answer_url from question WHERE question_id = '%s' and answer_url is not null"
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
    cur.close()
    db.close()


def trans(subject, li):
    for i in li:
        print(i)
        main(subject, i[0], i[1], i[2])


if __name__ == '__main__':
    li = [['课题1 金属材料', '060009002022100001001', '9861'], ['课题2 金属的化学性质', '060009002022100001002', '9862'],
          ['课题3 金属资源的利用和保护', '060009002022100001003', '9863'],
          ['实验活动4：金属的物理性质和某些化学性质', '060009002022100001004', '76881'], ['课题1 溶液的形成', '060009002022100002001', '9865'],
          ['课题2 溶解度', '060009002022100002002', '9866'], ['课题3 溶液的浓度', '060009002022100002003', '76882'],
          ['实验活动5：一定溶质质量分数的氯化钠溶液的配制', '060009002022100002004', '76883'],
          ['课题1 常见的酸和碱', '060009002022100003001', '9870'], ['课题2 酸和碱的中和反应', '060009002022100003002', '9871'],
          ['实验活动6：酸、碱的化学性质', '060009002022100003003', '76884'], ['实验活动7：溶液酸碱性的检验', '060009002022100003004', '76885'],
          ['课题1 生活中常见的盐', '060009002022100004001', '9873'], ['课题2 化学肥料', '060009002022100004002', '24814'],
          ['实验活动8：粗盐中难溶性杂质的去除', '060009002022100004003', '76886'], ['课题1 人类重要的营养物质', '060009002022100005001', '9876'],
          ['课题2 化学元素与人体健康', '060009002022100005002', '9877'], ['课题3 有机合成材料', '060009002022100005003', '9878']]
    for i in range(6):
        t = threading.Thread(target=trans, args=("hx", li[3 * i:3 * i + 3],))
        t.start()
