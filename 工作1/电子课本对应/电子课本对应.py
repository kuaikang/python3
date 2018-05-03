from common.mysql_util import mysql
from common.string_util import get_similarity
import re


def select_chapter(book_id):
    with mysql(db="sit_exue_resource") as cur:
        cur.execute("select * from t_res_chapter where book_id = '{book_id}'".format(book_id=book_id))
        return cur.fetchall()


def valid_name(name):
    parse = '0123456789、.《》（）'
    for item in parse:
        name = name.replace(item, '')
    return name


def parse_chapter():
    result = {}
    old = select_chapter("010002002104100")
    new = select_chapter("240008001728860")
    for o in old:
        for n in new:
            name1 = o.get('chapter_name')
            name2 = n.get('chapter_name')
            similarity = get_similarity(valid_name(name1), valid_name(name2))
            if similarity > 0.6:
                # print(name1, name2, similarity)
                result[o.get('chapter_id')] = n.get('chapter_id')
                break
    return result


def handle():
    pattern = re.compile(".*?jpg', '(\d+)',", re.S)
    result = parse_chapter()
    f = open("电子课本_new.txt", mode="r", encoding="utf8")
    f_new = open("电子课本_new.txt", mode="w", encoding="utf8")
    for line in f.readlines():
        old = re.findall(pattern, line)[0]
        print(old, result.get(old))
        f_new.write(line.replace(old, result.get(old)))
    f_new.close()
    f.close()


if __name__ == '__main__':
    print(parse_chapter())
