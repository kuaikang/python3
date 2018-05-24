from common.mysql_util import mysql
import time

sel_questions = "select * from t_res_{subject}_question WHERE create_time >= '2018-05-15' limit {start},1000"
sel_item = "select * from t_res_{subject}_item WHERE question_uuid = '{question_uuid}';"
sel_tag_question = "select * from t_res_{subject}_tag_question WHERE question_uuid = '{question_uuid}';"
sel_book = "SELECT * from t_res_chapter c LEFT JOIN t_res_graduate_book gb on c.book_id = gb.book_id LEFT JOIN " \
           "t_res_book b on b.book_id = c.book_id LEFT JOIN t_res_editor e on b.edition_id = e.edition_id " \
           "WHERE c.chapter_id = (SELECT ch.chapter_id from t_res_chapter ch LEFT JOIN t_res_{subject}_question_chapter qc " \
           "on ch.chapter_id = qc.chapter_id WHERE question_uuid = '{question_uuid}')"

# 查询题干或选项含有上标的题目
sel_questions_sup = "SELECT * from t_res_{subject}_question where uuid in (SELECT question_uuid as uuid from t_res_{subject}_item q " \
                    "where q.content like '%<sup%' and create_time >= '2018-05-15' " \
                    "or question_uuid in (SELECT uuid from t_res_sx_question q where q.context like '%<sup>%' " \
                    "and create_time >= '2018-05-15') GROUP BY question_uuid) limit {start},1000"
# 选项中含有换行标签的
sel_questions_item_br = "SELECT * from t_res_{subject}_question where uuid in (SELECT question_uuid as uuid " \
                        "from t_res_{subject}_item q where q.content like '%<br%' " \
                        "and create_time >= '2018-05-15' GROUP BY question_uuid) limit {start},1000;"

sel_questions_item_img = "SELECT * from t_res_{subject}_question where uuid in (SELECT question_uuid from t_res_{subject}_item " \
                         "where content like '%<img%' " \
                         "and create_time >= '2018-05-15' GROUP BY question_uuid) limit {start},1000;"


def show(subject, start):
    count = start * 1000 + 1
    options = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    with mysql(db="sit_exue_resource") as cur:
        # print(sel_questions.format(subject=subject, start=start * 1000))
        # cur.execute(sel_questions.format(subject=subject, start=start * 1000))
        print(sel_questions_item_img.format(subject=subject, start=start * 1000))
        cur.execute(sel_questions_item_img.format(subject=subject, start=start * 1000))
        questions = cur.fetchall()
        f = open("F:/html/{subject}_img{count}-{end}.html".format(subject=subject, count=count, end=count + 999),
                 mode="a",
                 encoding="utf8")
        f.write('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title></head><body>')
        for q in questions:
            html = ["第" + str(count) + '题, 题目ID：' + q.get('uuid') + ' ']
            cur.execute(sel_book.format(subject=subject, question_uuid=q.get('uuid')))
            data = cur.fetchone()
            if data:
                html.append(
                    data.get('subject_name') + '\t' + data.get('grade') + '年级' + '\t' + data.get(
                        'press_name') + data.get(
                        'edition_name') + '\t' + data.get('book_name') + '  章节：' + data.get('chapter_name') + '<br/>')
            cur.execute(sel_item.format(subject=subject, question_uuid=q.get('uuid')))
            items = cur.fetchall()
            cur.execute(sel_tag_question.format(subject=subject, question_uuid=q.get('uuid')))
            tags = cur.fetchall()
            html.append(q.get('context') + '<br/>')
            answer = ""
            for index, item in enumerate(items):
                if item.get('iscorrect') == 'Y':
                    answer = options[index]
                html.append(options[index] + ":" + item.get('content') + '<br/>')
            html.append("答案:" + answer + '<br/>')
            if tags:
                html.append("知识点:")
                data = [item.get('tag_name') for item in tags]
                html.append(",".join(data))
            html.append("<br/>")
            html.append("<br/>")
            html.append("<br/>")
            count += 1
            f.write("".join(html))
        f.write('</body></html')
        f.close()


if __name__ == '__main__':
    for i in range(1):
        start = time.time()
        show("sw", i)
        print(time.time() - start)
    print(time.time())