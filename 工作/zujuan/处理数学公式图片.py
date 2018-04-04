import pymysql
import requests
import re
import os
import threading


def get_db_sit():
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


def get_contexts_question(subject_key):
    db = get_db_sit()
    cur = db.cursor()
    cur.execute("select context from t_res_{}_question WHERE context like '%MathMLToImage%'".format(subject_key))
    data = cur.fetchall()
    cur.close()
    db.close()
    return data


def get_contents_item(subject_key):
    db = get_db_sit()
    cur = db.cursor()
    cur.execute("select content from t_res_{}_item WHERE content like '%MathMLToImage%'".format(subject_key))
    data = cur.fetchall()
    cur.close()
    db.close()
    return data


def parse_src(data):
    pattern = re.compile('.*?src="(.*?)"', re.S)
    src_set = set()
    for context in data:
        src = re.findall(pattern, context[0])
        for s in src:
            src_set.add(s)
    return src_set


def main(subject_key):
    contexts = get_contexts_question(subject_key)
    data = parse_src(contexts)
    for d in data:
        print(d)


if __name__ == '__main__':
    main("sx")
