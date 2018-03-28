import requests

if __name__ == '__main__':
    sql_unit = "INSERT INTO `kuaik`.`unit` (`unit_id`, `unit_name`, `book_id`) " \
               "VALUES ('{unit_id}', '{unit_name}', '{book_id}');"
    sql_chapter = "INSERT INTO `kuaik`.`chapter` (`chapter_id`, `chapter_name`, `unit_id`, `book_id`) " \
                  "VALUES ('{chapter_id}', '{chapter_name}', '{unit_id}', '{book_id}');"
    arr = [{"id": "6385", "title": "\u7b2c\u4e00\u7ae0 \u6253\u5f00\u7269\u7406\u4e16\u754c\u7684\u5927\u95e8"},
           {"id": "6386", "title": "\u7b2c\u4e8c\u7ae0 \u8fd0\u52a8\u7684\u4e16\u754c"},
           {"id": "6387", "title": "\u7b2c\u4e09\u7ae0 \u58f0\u7684\u4e16\u754c"},
           {"id": "6388", "title": "\u7b2c\u56db\u7ae0 \u591a\u5f69\u7684\u5149"},
           {"id": "77213", "title": "\u7b2c\u4e94\u7ae0 \u8d28\u91cf\u4e0e\u5bc6\u5ea6"},
           {"id": "6389", "title": "\u7b2c\u516d\u7ae0 \u719f\u6089\u800c\u964c\u751f\u7684\u529b"},
           {"id": "6390", "title": "\u7b2c\u4e03\u7ae0 \u529b\u4e0e\u8fd0\u52a8"},
           {"id": "6392", "title": "\u7b2c\u516b\u7ae0 \u538b\u5f3a"},
           {"id": "77212", "title": "\u7b2c\u4e5d\u7ae0 \u6d6e\u529b"},
           {"id": "6393", "title": "\u7b2c\u5341\u7ae0 \u673a\u68b0\u4e0e\u4eba"},
           {"id": "6394", "title": "\u7b2c\u5341\u4e00\u7ae0 \u5c0f\u7c92\u5b50\u4e0e\u5927\u5b87\u5b99"}]
    book_id = "6383"
    for item in arr:
        print(sql_unit.format(unit_id=item["id"], unit_name=item["title"], book_id=book_id))
        resp = requests.get("http://www.zujuan.com/question/tree?id=%s&type=category&_=1521177223714" % item["id"])
        for chapter in resp.json():
            print(sql_chapter.format(chapter_id=chapter["id"], chapter_name=chapter["title"], unit_id=item["id"],
                                     book_id=book_id))
