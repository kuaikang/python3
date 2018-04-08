import pymysql
import datetime
import contextlib


# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='123.206.227.74', port=3306, user='root', password='exue2017', db='sit_exue_resource', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    finally:
        conn.commit()
        cur.close()
        conn.close()


def item(subject_key):
    with mysql() as cursor:
        cursor.execute(
            "SELECT t.* from t_res_{subject_key}_item t "
            "LEFT JOIN t_res_{subject_key}_question q on t.question_uuid = q.uuid WHERE t.create_time > '2018-03-16 00:00:00' "
            "and q.context not like '%<table%' and t.question_uuid not in "
            "(SELECT question_uuid FROM t_res_{subject_key}_item WHERE content like '%<table%')".format(
                subject_key=subject_key))
        data = cursor.fetchall()
        insert_sql = "INSERT INTO `uat_exue_resource`.`t_res_{subject_key}_item` (`p_id`, `question_uuid`, `content`, `iscorrect`, `cor_code`, `option_code`, `create_time`) " \
                     "VALUES ('{p_id}', '{question_uuid}', '{content}', '{iscorrect}', NULL, NULL, '{create_time}') ON DUPLICATE KEY UPDATE p_id = VALUES (p_id);"
        f = open("sql/%s_item.txt" % subject_key, mode="a", encoding="utf8")
        print(len(data))
        for d in data:
            f.write(insert_sql.format(subject_key=subject_key, p_id=d.get('p_id'), question_uuid=d.get('question_uuid'),
                                      content=pymysql.escape_string(d.get('content')), iscorrect=d.get('iscorrect'),
                                      create_time=d.get('create_time').strftime('%Y-%m-%d %H:%M:%S')))
            f.write("\n")
        f.close()


def question(subject_key):
    with mysql() as cursor:
        cursor.execute(
            "SELECT q.* from t_res_{subject_key}_question q WHERE q.create_time > '2018-03-16 00:00:00' and q.context not like '%<table%' "
            "and q.uuid not in (SELECT question_uuid from t_res_{subject_key}_item where content like '%<table%')".format(
                subject_key=subject_key))
        data = cursor.fetchall()
        insert_sql = "INSERT INTO `uat_exue_resource`.`t_res_{subject_key}_question` (`uuid`, `context`, `item_attribute`, `item_id`, `publish_time`, `update_date`, " \
                     "`version`, `type`, `quality`, `create_time`) " \
                     "VALUES ('{uuid}', '{context}', NULL, NULL, '0', '{update_date}', '{version}', '{type}', '{quality}', '{create_time}') ON DUPLICATE KEY UPDATE uuid = VALUES (uuid);"
        f = open("sql/%s_question.txt" % subject_key, mode="a", encoding="utf8")
        print(len(data))
        for d in data:
            f.write(insert_sql.format(subject_key=subject_key, uuid=d.get('uuid'), context=d.get('context'),
                                      update_date=d.get('update_date'), version=d.get('version'), type=d.get('type'),
                                      quality=d.get('quality'),
                                      create_time=d.get('create_time').strftime('%Y-%m-%d %H:%M:%S')))
            f.write("\n")
        f.close()


def tag(subject_key):
    with mysql() as cursor:
        cursor.execute("SELECT * from t_res_{subject_key}_tag".format(subject_key=subject_key))
        data = cursor.fetchall()
        insert_sql = "INSERT INTO `uat_exue_resource`.`t_res_{subject_key}_tag` (`tag_id`, `tag_name`, `tag_description`, `tag_url`) " \
                     "VALUES ('{tag_id}', '{tag_name}', {tag_description}, NULL) ON DUPLICATE KEY UPDATE tag_id = VALUES (tag_id);"
        f = open("sql/%s_tag.txt" % subject_key, mode="a", encoding="utf8")
        print(len(data))
        for d in data:
            if not d.get('tag_description'):
                f.write(insert_sql.format(subject_key=subject_key, tag_id=d.get('tag_id'), tag_name=d.get('tag_name'),
                                          tag_description='NULL'))
            else:
                f.write(insert_sql.format(subject_key=subject_key, tag_id=d.get('tag_id'), tag_name=d.get('tag_name'),
                                          tag_description="'" + pymysql.escape_string(d.get('tag_description')) + "'"))
            f.write("\n")
        f.close()


def tag_question(subject_key):
    with mysql() as cursor:
        cursor.execute(
            "SELECT * from t_res_{subject_key}_tag_question WHERE create_time > '2018-03-16 00:00:00'".format(
                subject_key=subject_key))
        data = cursor.fetchall()
        insert_sql = "INSERT INTO `uat_exue_resource`.`t_res_{subject_key}_tag_question` (`tag_id`, `tag_name`, `question_uuid`, `create_time`) " \
                     "VALUES ('{tag_id}', '{tag_name}', '{question_uuid}', '{create_time}');"
        f = open("sql/%s_tag_question.txt" % subject_key, mode="a", encoding="utf8")
        print(len(data))
        for d in data:
            f.write(insert_sql.format(subject_key=subject_key, tag_id=d.get('tag_id'),
                                      tag_name=pymysql.escape_string(d.get('tag_name')),
                                      question_uuid=d.get('question_uuid'),
                                      create_time=d.get('create_time').strftime('%Y-%m-%d %H:%M:%S')))
            f.write("\n")
        f.close()


def chapter_question(subject_key):
    with mysql() as cursor:
        cursor.execute(
            "SELECT qc.* from t_res_{subject_key}_question_chapter qc LEFT JOIN t_res_{subject_key}_question q on qc.question_uuid = q.uuid "
            "WHERE qc.create_time > '2018-03-16 00:00:00' and q.context not like '%<table%' "
            "and qc.question_uuid not in (select question_uuid from t_res_{subject_key}_item WHERE content like '%<table%')".format(
                subject_key=subject_key))
        data = cursor.fetchall()
        insert_sql = "INSERT INTO `uat_exue_resource`.`t_res_{subject_key}_question_chapter` (`question_uuid`, `chapter_id`, `chapter_name`, `create_time`) " \
                     "VALUES ('{question_uuid}', '{chapter_id}', '{chapter_name}', '{create_time}');"
        f = open("sql/%s_chapter_question.txt" % subject_key, mode="a", encoding="utf8")
        print(len(data))
        for d in data:
            f.write(insert_sql.format(subject_key=subject_key, question_uuid=d.get('question_uuid'),
                                      chapter_id=d.get('chapter_id'),
                                      chapter_name=pymysql.escape_string(d.get('chapter_name')),
                                      create_time=d.get('create_time').strftime('%Y-%m-%d %H:%M:%S')))
            f.write("\n")
        f.close()


if __name__ == '__main__':
    keys = ['yw', 'sx', 'yy', 'ls', 'dl', 'wl', 'hx', 'sw']
    for key in keys:
        item(key)
        chapter_question(key)
        question(key)
        tag(key)
        tag_question(key)
