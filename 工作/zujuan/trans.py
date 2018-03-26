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
    li = [['6.1 从实际问题到方程', '020007002043100001001', '14880'], ['6.2 解一元一次方程', '020007002043100001002', '25210'],
          ['6.3 实践与探索', '020007002043100001003', '14883'], ['7.1 二元一次方程组和它的解', '020007002043100002001', '14884'],
          ['7.2 二元一次方程组的解法', '020007002043100002002', '14885'], ['7.3 三元一次方程组的解法', '020007002043100002003', '94144'],
          ['7.4 实践与探索', '020007002043100002004', '15959'], ['8.1 认识不等式', '020007002043100003001', '25212'],
          ['8.2 解一元一次不等式', '020007002043100003002', '25213'], ['8.3 一元一次不等式组', '020007002043100003003', '25214'],
          ['9.1 三角形', '020007002043100004001', '14887'], ['9.2 多边形的内角和与外角和', '020007002043100004002', '14890'],
          ['9.3 用正多边形铺设地面', '020007002043100004003', '14891'], ['10.1 轴对称', '020007002043100005001', '94146'],
          ['10.2 平移', '020007002043100005002', '94149'], ['10.3 旋转', '020007002043100005003', '94150'],
          ['10.4 中心对称', '020007002043100005004', '94151'], ['10.5 图形的全等', '020007002043100005005', '94152']]

    for i in range(6):
        t = threading.Thread(target=trans, args=("sx", li[3 * i:3 * i + 3],))
        t.start()
