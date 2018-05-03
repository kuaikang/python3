import os
import contextlib
import pymysql
import re
from common.string_util import get_similarity
from common.mysql_util import mysql


# 格式化名称
def valid_name(name):
    reg = re.compile(r'[\\/:*?".<>| 《》◎：0123456789\r\n]+')
    valid = reg.findall(name)
    if valid:
        for v in valid:
            name = name.replace(v, '')
    return name


# 比对2个名称
def cmp_str(str1, str2):
    num = get_similarity(valid_name(str1), valid_name(str2))
    if num >= 0.7:
        print(str1, str2, num)
        return True
    return False


# 根据课本获取所有的章节信息,返回字典{"chapter_id":"unit_id"}
def get_unit(book_id):
    with mysql(db="topic_standard_test") as cur:
        cur.execute("SELECT * from t_res_chapter WHERE book_id = '{book_id}';".format(book_id=book_id))
        return {item.get('chapter_id'): item.get('unit_id') for item in cur.fetchall()}


# 根据课本获取所有的章节信息,返回字典{"chapter_id":"unit_id"}
def get_chapter(book_id):
    with mysql(db="topic_standard_test") as cur:
        cur.execute("SELECT * from t_res_chapter WHERE book_id = '{book_id}';".format(book_id=book_id))
        return cur.fetchall()


# 修改章节名称为id,参数为课本路径
def modify_dir_name(path):
    book_id = os.path.split(path)[-1]
    chapters = get_chapter(book_id)
    chapter_dir = os.listdir(path)
    for chinese_name in chapter_dir:
        for c in chapters:
            if cmp_str(chinese_name, c.get('chapter_name')):  # 判断章节名是否相同
                old_name = os.path.join(path, chinese_name)
                new_name = old_name.replace(chinese_name, c.get('chapter_id'))
                os.rename(old_name, new_name)
                chapters.remove(c)
                break


if __name__ == '__main__':
    modify_dir_name("F:\\运营0426\\010002002104100")
