from flask import Flask, render_template, redirect, url_for, request, make_response
from common.db_util import OPMysql

app = Flask(__name__)
opm = OPMysql()


def select_question(subject, content, option=None):
    if subject and content:
        sql = 'select * from t_res_{subject}_question where type = "11" ' \
              'and context like "%{content}%" order by context limit 10'
        res = opm.op_select_all(sql.format(subject=subject, content=content))
        return res
    else:
        return None


select_option = "select * from t_res_{subject}_item where question_uuid = '{question_uuid}'"
select_chapter = "SELECT * from t_res_{subject}_question_chapter qc LEFT JOIN t_res_chapter c " \
                 "on qc.chapter_id = c.chapter_id LEFT JOIN t_res_book b on c.book_id = b.book_id " \
                 "LEFT JOIN t_res_editor e on b.edition_id = e.edition_id " \
                 "where question_uuid = '{question_uuid}'"


def select_options(subject, question_uuid):
    res = opm.op_select_all(select_option.format(subject=subject, question_uuid=question_uuid))
    return res


def select_chapters(subject, question_uuid):
    res = opm.op_select_all(select_chapter.format(subject=subject, question_uuid=question_uuid))
    return res


opt = ['A', 'B', 'C', 'D', 'E', 'F', 'G']


@app.route("/", methods=['POST', 'GET'])
def hello():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        questions = select_question(request.form['subject'], request.form['content'])
        for question in questions:
            options = select_options(request.form['subject'], question.get('uuid'))
            for index, item in enumerate(options):
                item['content'] = opt[index] + '：' + item.get('content')
                if item.get('iscorrect') == 'Y':
                    question['answer'] = opt[index]
            question['options'] = options
            question['chapters'] = select_chapters(request.form['subject'], question.get('uuid'))
        return render_template("index.html", questions=questions)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9527, debug=True)
