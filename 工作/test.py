import requests,os
import uuid
if __name__ == '__main__':
    # sql_unit = "INSERT INTO `kuaik`.`unit` (`unit_id`, `unit_name`, `book_id`) " \
    #            "VALUES ('{unit_id}', '{unit_name}', '{book_id}');"
    # sql_chapter = "INSERT INTO `kuaik`.`chapter` (`chapter_id`, `chapter_name`, `unit_id`, `book_id`) " \
    #               "VALUES ('{chapter_id}', '{chapter_name}', '{unit_id}', '{book_id}');"
    # arr = [{"id": "94994", "title": "\u7b2c\u4e94\u7ae0 \u4e2d\u56fd\u7684\u5730\u7406\u5dee\u5f02"},
    #        {"id": "94995", "title": "\u7b2c\u516d\u7ae0 \u5317\u65b9\u5730\u533a"},
    #        {"id": "94996", "title": "\u7b2c\u4e03\u7ae0 \u5357\u65b9\u5730\u533a"},
    #        {"id": "94997", "title": "\u7b2c\u516b\u7ae0 \u897f\u5317\u5730\u533a"},
    #        {"id": "94998", "title": "\u7b2c\u4e5d\u7ae0 \u9752\u85cf\u5730\u533a"},
    #        {"id": "94999", "title": "\u7b2c\u5341\u7ae0 \u4e2d\u56fd\u5728\u4e16\u754c\u4e2d"}]
    #
    # book_id = "4977"
    # for item in arr:
    #     print(sql_unit.format(unit_id=item["id"], unit_name=item["title"], book_id=book_id))
    #     resp = requests.get("http://www.zujuan.com/question/tree?id=%s&type=category&_=1521177223714" % item["id"])
    #     for chapter in resp.json():
    #         print(sql_chapter.format(chapter_id=chapter["id"], chapter_name=chapter["title"], unit_id=item["id"],
    #                                  book_id=book_id))
    os.makedirs("E:\\test\\te")