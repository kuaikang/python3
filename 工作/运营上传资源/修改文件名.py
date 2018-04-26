from common.mysql_util import mysql
import os
from common.string_util import valid_name, get_similarity


def change_unit(path):
    with mysql(db="topic_standard_test") as cur:
        books = os.listdir(path)
        for book in books:
            cur.execute("select * from t_res_units where book_id = '{book_id}'".format(book_id=book))
            res = cur.fetchall()
            units = os.listdir(os.path.join(path, book))
            for unit in units:
                for r in res:
                    if get_similarity(valid_name(r.get('unit_name')), valid_name(unit)) > 0.7:
                        print(r.get('unit_name'), unit)
                        res.remove(r)
                        old_name = path + '/' + book + '/' + unit
                        new_name = path + '/' + book + '/' + r.get('unit_id')
                        os.rename(old_name, new_name)
                        break


if __name__ == '__main__':
    # change_unit("F:/运营0423/yy")
    book_ids = os.listdir("F:/运营0423/yy")
    with mysql(db="topic_standard_test") as cur:
        for book_id in book_ids:
            book_path = os.path.join("F:/运营0423/yy", book_id)
            unit_ids = os.listdir(book_path)
            for unit_id in unit_ids:
                unit_path = os.path.join(book_path, unit_id)
                chapter_ids = os.listdir(unit_path)
                cur.execute("select * from t_res_chapter where unit_id='{unit_id}'".format(unit_id=unit_id))
                data = cur.fetchall()
                for chapter_id in chapter_ids:
                    chapter_path = os.path.join(unit_path, chapter_id)
                    for item in data:
                        if get_similarity(valid_name(item.get('chapter_name')), valid_name(chapter_id)) > 0.7:
                            new_name = os.path.join(unit_path, item.get('chapter_id'))
                            os.rename(chapter_path, new_name)
                            data.remove(item)
                            break
