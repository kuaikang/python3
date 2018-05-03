import os
from common.mysql_util import mysql

select_chapter = "select * from t_res_chapter where chapter_id = {chapter_id}"


def file_name(file_dir):
    with mysql(db="sit_exue_resource") as cur:
        for root, dirs, files in os.walk(file_dir):
            for d in dirs:
                if not d.isdigit(): continue
                cur.execute(select_chapter.format(chapter_id=d))
                data = cur.fetchone()
                if data:
                    print(os.path.join(root, d))
                    print(os.path.join(root, data.get('chapter_name')))


if __name__ == '__main__':
    for item in file_name("F:\\运营0426\\010002002104100"):
        print(item)
