import requests
import re
import os
import random
import uuid
import json
from common.mysql_util import mysql


def get_contexts_question(subject_key):
    with mysql(db="zujuan_spark_test") as cursor:
        cursor.execute("select context,uuid from t_res_{}_question WHERE context like '%MathMLToImage%' "
                       "and create_time >= '2018-04-17'".format(subject_key))
        return cursor.fetchall()


def get_contents_item(subject_key):
    with mysql(db="zujuan_spark_test") as cursor:
        cursor.execute("select content,question_uuid from t_res_{}_item WHERE content like '%MathMLToImage%' "
                       "and create_time >= '2018-04-17 00:00:00'".format(subject_key))
        return cursor.fetchall()


def parse_src(data):
    pattern = re.compile('.*?src="(.*?)"', re.S)
    src_set = set()
    for item in data:
        c = item.get('content') if item.get('content') else item.get('context')
        src = re.findall(pattern, c)
        for s in src:
            if 'MathMLToImage' in s:
                src_set.add(s)
    return src_set


def write_file(subject_key, resp):
    first = random_dir()
    second = random_dir()
    path = "F:/question_img_0419/{subject_key}/{first}/{second}".format(subject_key=subject_key, first=first,
                                                                        second=second)
    if not os.path.exists(path): os.makedirs(path)  # 假如路径不存在,就创建路径
    file_name = str(uuid.uuid4()).replace('-', '')
    file_type = resp.headers.get("Content-Type").split('/')[-1]
    new_path = "{path}/{file_name}.{file_type}".format(path=path, file_name=file_name, file_type=file_type)
    print(new_path)
    with open(new_path, mode="wb") as f:
        f.write(resp.content)
    return new_path


def random_dir():
    li = []
    for i in range(3):
        li.append(chr(random.randint(65, 90)).lower())
        li.append(str(random.randint(0, 9)))
    return "".join(random.sample(li, 2))


f = open("F:/img.txt", mode="a", encoding="utf8")


def src_handle(subject_key, contexts):
    data = parse_src(contexts)
    print(len(data))
    with requests.session() as session:
        for item in data:
            resp = session.get(item)
            if resp.status_code == 200:
                new_path = write_file(subject_key, resp)
                f.write(json.dumps({item: new_path}, ensure_ascii=False))
                f.write("\n")
            else:
                print(key)


def main(subject_key):
    contexts = get_contexts_question(subject_key)
    src_handle(subject_key, contexts)
    contents = get_contents_item(subject_key)
    src_handle(subject_key, contents)


if __name__ == '__main__':
    # subject_keys = ['yw', 'yy', 'sx', 'ls', 'dl', 'wl', 'hx', 'sw']
    subject_keys = ['wl']
    for key in subject_keys:
        print(key)
        main(key)
    f.close()
