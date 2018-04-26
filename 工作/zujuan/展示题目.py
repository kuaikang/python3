from common.mysql_util import mysql
import time

sel_questions = "select * from t_res_{subject}_question WHERE create_time >= '2018-04-25' limit {start},1000"
sel_item = "select * from t_res_{subject}_item WHERE question_uuid = '{question_uuid}';"
sel_tag_question = "select * from t_res_{subject}_tag_question WHERE question_uuid = '{question_uuid}';"
sel_book = "SELECT * from t_res_book b LEFT JOIN t_res_graduate_book gb on b.book_id = gb.book_id LEFT JOIN t_res_editor e " \
           "on b.edition_id = e.edition_id WHERE b.book_id = (SELECT c.book_id from t_res_chapter c LEFT JOIN t_res_{subject}_question_chapter qc " \
           "on c.chapter_id = qc.chapter_id WHERE question_uuid = '{question_uuid}')"


def show(subject, start):
    count = start * 1000 + 1
    options = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    with mysql(db="sit_exue_resource") as cur:
        print(sel_questions.format(subject=subject, start=start * 1000))
        cur.execute(sel_questions.format(subject=subject, start=start * 1000))
        questions = cur.fetchall()
        f = open("F:/html/{subject}{count}-{end}.html".format(subject=subject, count=count, end=count + 999), mode="a",
                 encoding="utf8")
        f.write('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title></head><body>')
        for q in questions:
            html = ["第" + str(count) + '题:']
            cur.execute(sel_book.format(subject=subject, question_uuid=q.get('uuid')))
            data = cur.fetchone()
            if data:
                html.append(
                    data.get('subject_name') + ' ' + data.get('grade') + '年级' + ' ' + data.get('press_name') + data.get(
                        'edition_name') + ' ' + data.get('book_name') + '<br/>')
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
    for i in range(7):
        start = time.time()
        show("sx", i)
        print(time.time() - start)
