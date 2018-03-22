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
    li = [['第2课 原始农耕生活', '100007001620337001002', '119451'],
          ['第3课 远古的传说', '100007001620337001003', '119452'], ['第4课 早期国家的产生和发展', '100007001620337002001', '119454'],
          ['第5课 青铜器与甲骨文', '100007001620337002002', '119456'], ['第6课 动荡的春秋时期', '100007001620337002003', '119457'],
          ['第7课 战国时期的社会变化', '100007001620337002004', '119458'], ['第8课 百家争鸣', '100007001620337002005', '119461'],
          ['第9课 秦统一中国', '100007001620337003001', '119463'], ['第10课 秦末农民大起义', '100007001620337003002', '119464'],
          ['第11课 西汉建立和“文景之治”', '100007001620337003003', '119465'],
          ['第12课 汉武帝巩固大统一王朝', '100007001620337003004', '119466'], ['第13课 东汉的兴亡', '100007001620337003005', '119467'],
          ['第14课 沟通中外文明的“丝绸之路”', '100007001620337003006', '119468'],
          ['第15课 两汉的科技和文化', '100007001620337003007', '119470'], ['第16课 三国鼎立', '100007001620337004001', '119472'],
          ['第17课 西晋的短暂统一和北方各族的内迁', '100007001620337004002', '119474'],
          ['第18课 东晋南朝时期江南地区的开发', '100007001620337004003', '119475'],
          ['第19课 北魏政治与北方民族大交融', '100007001620337004004', '119476'],
          ['第20课 魏晋南北朝的科技与文化', '100007001620337004005', '119477']]
    start_time = time.time()
    for i in li:
        print(i)
        main("ls", i[0], i[1], i[2])
    print(time.time() - start_time)
