import requests
import pymysql, time, threading
import contextlib


# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql_local(host='localhost', port=3333, user='root', password='kuaikang', db='kuaik', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)
    conn.autocommit(True)
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    finally:
        conn.commit()
        cur.close()
        conn.close()


def get_question_ids(subject_key, chapter_id):
    with mysql_local() as cur:
        sql = "SELECT question_id from {subject_key}_chapter_question WHERE chapter_id = '{chapter_id}'"
        cur.execute(sql.format(subject_key=subject_key, chapter_id=chapter_id))
        return cur.fetchall()


def get_question(subject_key, question_id):
    with mysql_local() as cur:
        sql = "SELECT context,type,difficult,answer_url from {subject_key}_question WHERE question_id = '{question_id}' and answer_url is not null"
        cur.execute(sql.format(subject_key=subject_key, question_id=question_id))
        return cur.fetchall()


def get_tag(subject_key, question_id):
    with mysql_local() as cur:
        sql = "SELECT tag_url from {subject_key}_tag_question WHERE question_id = '{question_id}'"
        cur.execute(sql.format(subject_key=subject_key, question_id=question_id))
        return cur.fetchone()


def get_item(subject_key, question_id):
    with mysql_local() as cur:
        sql = "SELECT content,`option` from {subject_key}_item WHERE question_id = '{question_id}'"
        cur.execute(sql.format(subject_key=subject_key, question_id=question_id))
        return cur.fetchall()


def main(currentSubject, importChapterName, import_Chapter, zujuan_chapter):
    head = {
        "Content-Type": "application/json"
    }
    with mysql_local() as cur:
        question_ids = get_question_ids(currentSubject, zujuan_chapter)
        for question_id in question_ids:
            question = get_question(cur, question_id.get('question_id'))
            for q in question:  # context,type,difficult,answer_url
                req = {"currentSubject": currentSubject, "questionContent": q.get('context'), "importChapterId": import_Chapter,
                       "questionType": "11"}
                tag = get_tag(currentSubject, question_id.get('question_id'))
                req["tagUrl"] = tag.get('tag_url')
                req["importChapterName"] = importChapterName
                req["answerUrl"] = q.get('answer_url')
                req["difficult"] = q.get('difficult')
                items = get_item(cur, question_id.get('question_id'))
                item = []
                for it in items:  # content,`option`
                    item.append({"content": it.get('content'), "option": it.get('option')})
                req["items"] = item
                requests.post(url="http://localhost:28870/exue-question-system/spark/save", headers=head, json=req)


def trans(subject, data):
    for d in data:
        print(i)
        main(subject, d[0], d[1], d[2])


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
        t = threading.Thread(target=trans, args=("yy", li[3 * i:3 * i + 3],))
        t.start()
