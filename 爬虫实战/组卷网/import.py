import contextlib
import pymysql
import uuid


@contextlib.contextmanager
def mysql(host='localhost', port=3333, user='root', password='kuaikang', db='kuaik', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)
    conn.autocommit(True)
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    finally:
        conn.commit()
        cur.close()
        conn.close()


def get_question_ids(cur, subject_key, chapter_id):
    sql = "SELECT question_id from {subject_key}_chapter_question WHERE chapter_id = '{chapter_id}'"
    cur.execute(sql.format(subject_key=subject_key, chapter_id=chapter_id))
    return cur.fetchall()


def get_question(cur, subject_key, question_id):
    sql = "SELECT context,question_type,difficult,answer_url from {subject_key}_question WHERE question_id = '{question_id}' and answer_url is not null"
    cur.execute(sql.format(subject_key=subject_key, question_id=question_id))
    return cur.fetchone()


def get_tag(cur, subject_key, question_id):
    sql = "SELECT tag_url from {subject_key}_tag_question WHERE question_id = '{question_id}'"
    cur.execute(sql.format(subject_key=subject_key, question_id=question_id))
    return cur.fetchone()


def get_item(cur, subject_key, question_id):
    sql = "SELECT context,`option` from {subject_key}_item WHERE question_id = '{question_id}'"
    cur.execute(sql.format(subject_key=subject_key, question_id=question_id))
    return cur.fetchall()


def create_uuid():
    return str(uuid.uuid4()).replace('-', '')


insert_question = "INSERT INTO `zujuan_spark_test`.`t_res_{subject_key}_question` (`uuid`, `context`, `publish_time`, `update_date`, " \
                  "`version`, `type`, `quality`, `answer_url`, `difficult`, `create_time`) VALUES ('{uuid}', '{content}', '0', now(), " \
                  "'1', '{type}', '5', '{answer_url}', '{difficult]', now());"
insert_item = "INSERT INTO `zujuan_spark_test`.`t_res_wl_item` (`p_id`, `question_uuid`, `content`, `create_time`, `question_option`) " \
              "VALUES ('{item_id}', '{question_uuid}', '{content}', NULL, NULL, NULL, now(), '{question_option}');"
insert_question_chapter = "INSERT INTO `zujuan_spark_test`.`t_res_wl_question_chapter` (`question_uuid`, `chapter_id`, `chapter_name`, `create_time`) " \
                          "VALUES ('{question_uuid}', '{chapter_id}', '{chapter_name}', now());"
insert_tag_question = "INSERT INTO `zujuan_spark_test`.`t_res_wl_tag_question` (`tag_id`, `tag_name`, `question_uuid`, `create_time`) " \
                      "VALUES ('{tag_id}', '{tag_name}', '{question_uuid}', now());"
insert_tag = "INSERT INTO `zujuan_spark_test`.`t_res_wl_tag` (`tag_id`, `tag_name`, `tag_description`, `tag_url`) " \
             "VALUES ('{tag_id]', '{tag_name}', NULL, '{tag_url}');"


def main(subject_key, chapter_id):
    with mysql() as cur:
        question_ids = get_question_ids(cur, subject_key, chapter_id)
        for ids in question_ids:
            question = get_question(cur, subject_key, ids.get('question_id'))
            print(question)


if __name__ == '__main__':
    data = [['第一节 运动和静止', '050008001142100002001', '91515']]
    for item in data:
        main("wl", item[2])
