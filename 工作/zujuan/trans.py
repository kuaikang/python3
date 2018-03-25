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
    li1 = [['第一节 温度与温度计', '050009001060100001001', '93165'], ['第二节 熔化与凝固', '050009001060100001002', '93166'],
           ['第三节 汽化与液化', '050009001060100001003', '93167'], ['第四节 升华与凝华', '050009001060100001004', '93168'],
           ['第五节 全球变暖与水资源危机', '050009001060100001005', '93169'], ['第一节 物体的内能', '050009001060100002001', '6464'],
           ['第一节 能量的转化与守恒', '050009001060100009001', '93683'], ['第二节 能源的开发和利用', '050009001060100009002', '93684'],
           ['第三节 材料的开发和利用', '050009001060100009003', '93685']]
    li2 = [['第二节 科学探究：物质的比热容', '050009001060100002002', '6465'], ['第三节 内燃机', '050009001060100002003', '6466'],
           ['第四节 热机效率和环境保护', '050009001060100002004', '6467'], ['第一节 电是什么', '050009001060100003001', '6469'],
           ['第二节 让电灯发光', '050009001060100003002', '6470'], ['第三节 连接串联电路和并联电路', '050009001060100003003', '6471'],
           ['第四节 科学探究：串联和并联电路的电流', '050009001060100003004', '6472'], ['第五节 测量电压', '050009001060100003005', '6473'],
           ['第一节 电阻和变阻器', '050009001060100004001', '6475'], ['第二节 科学探究：欧姆定律', '050009001060100004002', '6476']]
    li3 = [['第三节 “伏安法”测电阻', '050009001060100004003', '6477'], ['第四节 电阻的串联和并联', '050009001060100004004', '6478'],
           ['第五节 家庭用电', '050009001060100004005', '6479'], ['第一节 电流做功', '050009001060100005001', '93171'],
           ['第二节 电流做功的快慢', '050009001060100005002', '93172'], ['第三节 测量电功率', '050009001060100005003', '93173']]
    li4 = [['第四节 科学探究：电流的热效应', '050009001060100005004', '93174'], ['第一节 磁是什么', '050009001060100006001', '6485'],
           ['第二节 电流的磁场', '050009001060100006002', '6486'], ['第三节 科学探究：电动机为什么会转动', '050009001060100006003', '6487'],
           ['第一节 电能的产生', '050009001060100007001', '6489'], ['第二节 科学探究：怎样产生感应电流', '050009001060100007002', '6490'],
           ['第三节 电能的输送', '050009001060100007003', '6491'], ['第一节 感受信息', '050009001060100008001', '6493'],
           ['第二节 让信息“飞”起来', '050009001060100008002', '6494'], ['第三节 踏上信息高速公路', '050009001060100008003', '6495']]

    t1 = threading.Thread(target=trans, args=("wl", li1,))
    t1.start()
    t2 = threading.Thread(target=trans, args=("wl", li2,))
    t2.start()
    t3 = threading.Thread(target=trans, args=("wl", li3,))
    t3.start()
    t4 = threading.Thread(target=trans, args=("wl", li4,))
    t4.start()
