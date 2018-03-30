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
def get_question_not_answer(subject_key):
    db = get_db_spark()
    cur = db.cursor()
    cur.execute('SELECT uuid FROM t_res_sx_question WHERE answer ="资源路径错误" LIMIT 300')
    # cur.execute('SELECT uuid FROM t_res_%s_question WHERE LENGTH(answer) > 1' % subject_key)
    # cur.execute("SELECT uuid FROM t_res_{subject_key}_question WHERE answer is null or answer like '%资源%';".format(
    #     subject_key=subject_key))
    # cur.execute("SELECT a.question_uuid FROM (SELECT question_uuid,COUNT(*) AS n FROM t_res_yw_item GROUP BY question_uuid) a ORDER BY a.n DESC LIMIT 1")
    cur.execute("SELECT uuid from t_res_hx_question WHERE uuid = '62a5f61da74c48869a2f2e7f47f887f3'")
    return cur.fetchall()


def delete(subject_key, question_ids):
    db = get_db_spark()
    cur = db.cursor()
    res = [x[0] for x in question_ids]
    in_p = ', '.join((map(lambda x: '%s', res)))
    # 删除选项
    cur.execute(
        "DELETE from t_res_%s_item WHERE question_uuid in (%s)" % (subject_key, in_p), res)
    # 删除题目
    cur.execute("DELETE from t_res_%s_question WHERE uuid in (%s)" % (subject_key, in_p), res)
    # 删除章节题目关系
    cur.execute("DELETE from t_res_%s_question_chapter WHERE question_uuid in (%s)" % (subject_key, in_p), res)
    db.commit()
    for question_id in question_ids:
        question_id = question_id[0]
        # 查询知识点
        cur.execute(
            "SELECT tag_id from t_res_{subject_key}_tag_question WHERE question_uuid = '{question_uuid}'".format(
                subject_key=subject_key, question_uuid=question_id))
        tags = cur.fetchall()
        for t in tags:
            # 删除知识点
            cur.execute("DELETE from t_res_{subject_key}_tag WHERE tag_id = '{tag_id}'".format(subject_key=subject_key,
                                                                                               tag_id=t[0]))
        # 删除知识点章节对应关系
        cur.execute("DELETE from t_res_{subject_key}_tag_question WHERE question_uuid = '{question_uuid}'".format(
            subject_key=subject_key, question_uuid=question_id))
        db.commit()
    cur.close()
    db.close()


if __name__ == '__main__':
    data = get_question_not_answer('hx')
    delete('hx', data)
