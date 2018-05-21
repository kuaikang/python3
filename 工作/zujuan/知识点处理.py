import pymysql
import time


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


def get_db_topic():
    # 打开数据库连接
    try:
        db = pymysql.connect(
            host="123.206.227.74", user="root",
            password="exue2017", db="sit_exue_resource", port=3306,
            charset="utf8"
        )
        return db
    except Exception as e:
        print(e)


def insert_tag(subject_key):
    db_spark = get_db_spark()
    cur_spark = db_spark.cursor()
    db_topic = get_db_topic()
    cur_topic = db_topic.cursor()
    cur_spark.execute("select tag_description from t_res_%s_tag" % subject_key)
    result = cur_spark.fetchall()
    s = set()
    for res in result:
        tags = res[0].split(";")
        for tag in tags:
            if tag == '': continue
            s.add(tag.replace("\n", "").strip())
    sql_insert_tag = "INSERT INTO t_res_{subject_key}_tag_copy (`tag_id`, `tag_name`) " \
                     "VALUES ('{tag_id}', '{tag_name}');"
    tag_id = 2150000
    for i in s:
        cur_topic.execute(
            "select tag_id from t_res_%s_tag where tag_name = '%s'" % (subject_key, pymysql.escape_string(i)))
        data = cur_topic.fetchone()
        if data:
            cur_spark.execute(
                sql_insert_tag.format(subject_key=subject_key, tag_id=data[0], tag_name=pymysql.escape_string(i)))
        else:
            cur_spark.execute(
                sql_insert_tag.format(subject_key=subject_key, tag_id=tag_id, tag_name=pymysql.escape_string(i)))
            tag_id += 1
        db_spark.commit()
    cur_spark.close()
    db_spark.close()


def main(subject_key):
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    db = get_db_spark()
    cur = db.cursor()
    sql = "select tag_id,question_uuid from t_res_%s_tag_question ORDER BY tag_id" % subject_key
    print(sql)
    select_tag_by_id = "select tag_description from t_res_%s_tag where tag_id = %s"
    select_tag_by_name = "select tag_id from t_res_%s_tag_copy where tag_name = '%s'"
    insert_tag_question = "INSERT INTO t_res_{subject_key}_tag_question_copy (`tag_id`, `tag_name`, `question_uuid`, `create_time`) " \
                          "VALUES ('{tag_id}', '{tag_name}', '{question_uuid}', '{create_time}');"
    cur.execute(sql)
    tag_question_map = cur.fetchall()
    for m in tag_question_map:
        cur.execute(select_tag_by_id % (subject_key, m[0]))
        tag_name = cur.fetchone()
        if not tag_name: continue
        tag_list = tag_name[0].replace("\n", "").split(";")
        for t in tag_list:
            cur.execute(select_tag_by_name % (subject_key, t))
            tag_id = cur.fetchone()
            if not tag_id: continue
            cur.execute(
                "SELECT * FROM `t_res_{subject_key}_tag_question_copy` WHERE tag_id = '{tag_id}' and question_uuid = '{question_uuid}'".format(
                    subject_key=subject_key, tag_id=tag_id[0], question_uuid=m[1]))
            if not cur.fetchone():
                cur.execute(
                    insert_tag_question.format(subject_key=subject_key, tag_id=tag_id[0], tag_name=t,
                                               question_uuid=m[1], create_time=create_time
                                               ))
        db.commit()
    cur.close()
    db.close()


if __name__ == '__main__':
    # insert_tag('sw')
    main('sw')
