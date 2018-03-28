import pymysql


def get_db_spark():
    # 打开数据库连接
    try:
        db = pymysql.connect(
            host="123.206.227.74", user="root",
            password="exue2017", db="zujuan_spark_test", port=3306,
            charset="utf8"
        )
        return db
    except Exception as e:
        print(e)


# 得到没解析的题目id
def get_question_not_answer():
    db = get_db_spark()
    cur = db.cursor()
    cur.execute('SELECT uuid FROM t_res_sx_question WHERE answer is null LIMIT 500')
    return cur.fetchall()


def delete(question_ids):
    db = get_db_spark()
    cur = db.cursor()
    res = [x[0] for x in question_ids]
    in_p = ', '.join((map(lambda x: '%s', res)))
    # 删除选项
    cur.execute(
        "DELETE from t_res_sx_item WHERE question_uuid in (%s)" % in_p, res)
    # 删除题目
    cur.execute("DELETE from t_res_sx_question WHERE uuid in (%s)" % in_p, res)
    # 删除章节题目关系
    cur.execute("DELETE from t_res_sx_question_chapter WHERE question_uuid in (%s)" % in_p, res)
    db.commit()
    for question_id in question_ids:
        question_id = question_id[0]
        # 查询知识点
        cur.execute("SELECT tag_id from t_res_sx_tag_question WHERE question_uuid = '{question_uuid}'".format(
            question_uuid=question_id))
        tags = cur.fetchall()
        for t in tags:
            # 删除知识点
            cur.execute("DELETE from t_res_sx_tag WHERE tag_id = '{tag_id}'".format(tag_id=t[0]))
        # 删除知识点章节对应关系
        cur.execute("DELETE from t_res_sx_tag_question WHERE question_uuid = '{question_uuid}'".format(
            question_uuid=question_id))
        db.commit()
    cur.close()
    db.close()


if __name__ == '__main__':
    for i in range(30):
        data = get_question_not_answer()
        delete(data)
