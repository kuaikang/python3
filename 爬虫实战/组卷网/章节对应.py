import pymysql
import contextlib


# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='localhost', port=3333, user='root', password='kuaikang', db='kuaik', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)
    conn.autocommit(True)
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    finally:
        conn.commit()
        cur.close()
        conn.close()


def valid_name(name):
    useless = "、（）()\r\n——"
    for u in useless:
        name = name.replace(u, '')
    return name[1:]


def main(res_book_id, zujuan_book_id):
    with mysql(host="123.206.227.74", user="root",
               password="exue2017", db="topic_standard_test", port=3306) as cur_topic:
        sql = "SELECT chapter_name,chapter_id FROM t_res_chapter WHERE book_id = '{res_book_id}'"
        cur_topic.execute(sql.format(res_book_id=res_book_id))
        data1 = cur_topic.fetchall()
    with mysql(host="localhost", user="root",
               password="kuaikang", db="kuaik", port=3333) as cur_zu:
        sql = "SELECT chapter_id,chapter_name from chapter WHERE book_id = '{zujuan_book_id}'"
        cur_zu.execute(sql.format(zujuan_book_id=zujuan_book_id))
        data2 = cur_zu.fetchall()
    result = []
    for data in data1:
        flag = True
        for item in data2:
            if valid_name(data.get('chapter_name')) == valid_name(item.get('chapter_name')):
                result.append([data.get('chapter_name'), data.get('chapter_id'), item.get('chapter_id')])
                flag = False
        if flag:
            print(data.get('chapter_name'))
    return result


if __name__ == '__main__':
    # book_id, zuJuan_book_id = '030003002008040', "77399"  # 英语译林牛津版三下
    # book_id, zuJuan_book_id = '030004002008040', "28459"  # 英语译林牛津版四下
    # book_id, zuJuan_book_id = '030005002008040', "28461"  # 英语译林牛津版五下
    # book_id, zuJuan_book_id = '030006002008040', "28463"  # 英语译林牛津版六下

    # book_id, zuJuan_book_id = '030003002007038', "11424"  # 英语人教版三下（PEP版）
    # book_id, zuJuan_book_id = '030004002007038', "12294"  # 英语人教版四下（PEP版）
    # book_id, zuJuan_book_id = '030005002007038', "12296"  # 英语人教版五下（PEP版）
    # book_id, zuJuan_book_id = '030006002007038', "12298"  # 英语人教版六下（PEP版）

    # book_id, zuJuan_book_id = '030003002009042', "12722"  # 英语外研版三下（三年级起点）
    # book_id, zuJuan_book_id = '030004002009042', "12724"  # 英语外研版四下（三年级起点）
    # book_id, zuJuan_book_id = '030005002009042', "12726"  # 英语外研版五下（三年级起点）
    # book_id, zuJuan_book_id = '030006002009042', "12728"  # 英语外研版六下（三年级起点）

    # book_id, zuJuan_book_id = '030003002017100', "48487"  # 英语冀教版三下（三年级起点）
    # book_id, zuJuan_book_id = '030004002017100', "87436"  # 英语冀教版四下（三年级起点）
    # book_id, zuJuan_book_id = '030005002017100', "48491"  # 英语冀教版五下（三年级起点）
    # book_id, zuJuan_book_id = '030006002017100', "48493"  # 英语冀教版六下（三年级起点）

    # book_id, zuJuan_book_id = '050008001142100', "35490"  # 物理鲁科版八上
    # book_id, zuJuan_book_id = '050008002142100', "35544"  # 物理鲁科版八下
    # book_id, zuJuan_book_id = '050008002142100', "35544"  # 物理鲁科版九上
    # book_id, zuJuan_book_id = '050009002142100', "35566"  # 物理鲁科版九下
    data_0417 = [
        # ['050008001142100', '35490'],  # 物理鲁科版八上
        # ['050008002142100', '35544'],  # 物理鲁科版八下
        # ['050009001142100', '35555'],  # 物理鲁科版九上
        # ['050009002142100', '35566'],  # 物理鲁科版九下
        ['020001001004034', '3807'],  # 一年级上册
        ['020001002004034', '3808'],  # 一年级下册
        ['020002001004034', '3809'],  # 二年级上册
        ['020002002004034', '3810'],  # 二年级下册
        ['020003001004034', '3811'],  # 三年级上册
        ['020003002004034', '3812'],  # 三年级下册
        ['020004001004034', '3813'],  # 四年级上册
        ['020004002004034', '3814'],  # 四年级下册
        ['020005001004034', '3815'],  # 五年级上册
        ['020005002004034', '3816'],  # 五年级下册
        ['020006001004034', '3817'],  # 六年级上册
        ['020006002004034', '3818'],  # 六年级下册
    ]
    result = []
    for data in data_0417:
        res = main(data[0], data[1])
        print(res)
        for r in res:
            result.append(r)
    print(result)
    print(len(result))
