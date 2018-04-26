import pymysql
import contextlib
import uuid


# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='192.168.121.159', port=42578, user='juzi_emp', password='exue2018', db='uat_exue_resource',
          charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    finally:
        conn.commit()
        cur.close()
        conn.close()


def get_data(file_name):
    chapter = []
    with open(file_name, mode="r", encoding="utf8") as f:
        for line in f.readlines():
            line = line.strip().split(",")
            chapter.append(line)
    return chapter


def valid_name(name):
    parse = '0123456789、.'
    for item in parse:
        name = name.replace(item, '')
    return name


def main_question():
    chapter1 = get_data("语文湘教版二上（标准版）.txt")
    chapter2 = get_data("语文湘教版二上（2017）.txt")
    sql = "SELECT * from t_res_yw_question_chapter WHERE chapter_id = '{chapter_id}';"

    insert_cq = "INSERT INTO `sit_exue_resource`.`t_res_yw_question_chapter` (`question_uuid`, `chapter_id`, `chapter_name`, `create_time`) " \
                "VALUES ('{question_uuid}', '{chapter_id}', '{chapter_name}', '2018-04-19 13:32:40');"
    f = open("语文湘教版二上2017_sql_normal.txt", mode="a", encoding="utf8")
    with mysql() as cur:
        for ch1 in chapter1:
            if ch1[1] == '写话': continue
            for ch2 in chapter2:
                if ch1[2] == ch2[2] and valid_name(ch1[1]) == valid_name(ch2[1]):
                    cur.execute(sql.format(chapter_id=ch1[0]))
                    data = cur.fetchall()
                    if data:
                        print(ch1[0], ch1[1], ch2[0], ch2[1])
                        for d in data:
                            f.write(insert_cq.format(question_uuid=d.get('question_uuid'), chapter_id=ch2[0],
                                                     chapter_name=ch2[1]))
                            f.write("\n")
                    break
    f.close()


def main_resource():
    chapter1 = get_data("语文湘教版二下.txt")
    chapter2 = get_data("语文湘教版二下（2017）.txt")
    sql = "SELECT * from t_exue_resource_yw WHERE chapter_id = '{chapter_id}';"
    f_res = open("语文湘教版二下_res_normal.txt", mode="r", encoding="utf8")
    res_sql = f_res.readlines()
    f_res.close()
    f_res_new = open("语文湘教版二下_res_normal_new.txt", mode="a", encoding="utf8")
    with mysql() as cur:
        for ch1 in chapter1:
            if ch1[1] == '写话': continue
            for ch2 in chapter2:
                if ch1[2] == ch2[2] and valid_name(ch1[1]) == valid_name(ch2[1]):
                    cur.execute(sql.format(chapter_id=ch1[0]))
                    data = cur.fetchall()
                    if data:
                        for line in res_sql:
                            if ch1[0] in line:
                                line = line.replace(ch1[0], ch2[0]).replace('010002002012045', '240008001728759') \
                                    .replace('2017-12-15 19:30:13', '2018-04-19 12:12:12')
                                f_res_new.write(line)
                        print(ch1[0], ch1[1], ch2[0], ch2[1])
                    break
    f_res_new.close()


if __name__ == '__main__':
    # main_resource()
    f = open("语文湘教版二上_res_normal_new.txt",mode="r",encoding="utf8")
    f_new = open("语文湘教版二上_res_normal_new_1.txt",mode="w",encoding="utf8")
    for line in f.readlines():
        f_new.write(line.replace("UUID()",str(uuid.uuid4()).replace('-','')))
    f_new.close()
    f.close()