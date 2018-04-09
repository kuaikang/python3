import pymysql
import requests
import re
import os
import contextlib
import random
import uuid


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


def get_contexts_question(subject_key):
    with mysql() as cursor:
        cursor.execute("select context,uuid from t_res_{}_question WHERE context like '%MathMLToImage%' "
                       "and create_time >= '2018-03-16' and create_time <= '2018-04-02'".format(subject_key))
        return cursor.fetchall()


def get_contents_item(subject_key):
    with mysql() as cursor:
        cursor.execute("select content,question_uuid from t_res_{}_item WHERE content like '%MathMLToImage%' "
                       "and create_time >= '2018-03-16' and create_time <= '2018-04-02'".format(subject_key))
        return cursor.fetchall()


def parse_src(data):
    pattern = re.compile('.*?src="(.*?)"', re.S)
    src_set = set()
    for item in data:
        c = item.get('content') if item.get('content') else item.get('context')
        src = re.findall(pattern, c)
        for s in src:
            src_set.add(s)
    return src_set


def write_file(subject_key, resp):
    first = random_dir()
    second = random_dir()
    path = "E:/question_src/{subject_key}/{first}/{second}".format(subject_key=subject_key, first=first,
                                                                   second=second)
    if not os.path.exists(path): os.makedirs(path)  # 假如路径不存在,就创建路径
    file_name = str(uuid.uuid4()).replace('-', '')
    file_type = resp.headers.get("Content-Type").split('/')[-1]
    path_img = "{path}/{file_name}.{file_type}".format(path=path, file_name=file_name, file_type=file_type)
    print(path_img)
    with open(path_img, mode="wb") as f:
        f.write(resp.content)


def random_dir():
    li = []
    for i in range(3):
        li.append(chr(random.randint(65, 90)).lower())
        li.append(str(random.randint(0, 9)))
    return "".join(random.sample(li, 2))


def src_handle(subject_key, contexts):
    data = parse_src(contexts)
    print(len(data))
    with requests.session() as session:
        for src in data:
            resp = session.get(src)
            if resp.status_code == 200:
                # write_file(subject_key, resp)
                pass
            else:
                print(src)


def main(subject_key):
    contexts = get_contexts_question(subject_key)
    src_handle(subject_key, contexts)
    contents = get_contents_item(subject_key)
    src_handle(subject_key, contents)


if __name__ == '__main__':
    subject_keys1 = ['yw', 'yy', 'ls', 'dl', 'wl', 'hx', 'sw']
    subject_keys = ['sx']
    for key in subject_keys:
        print(key)
        main(key)
# 7990 + 10430
