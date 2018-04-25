import pymysql
import contextlib
from common.string_util import get_similarity


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
    useless = "、（）().\r\n——"
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
            if get_similarity(valid_name(data.get('chapter_name')), valid_name(item.get('chapter_name'))) > 0.7:
                result.append([data.get('chapter_name'), data.get('chapter_id'), item.get('chapter_id')])
                flag = False
        if flag:
            print(data.get('chapter_name'))
    return result


def update_chapter(data):
    sql = "update chapter set res_chapter_id = '{0}',res_chapter_name='{1}' WHERE chapter_id = {2};"
    for d in data:
        print(sql.format(d[1], pymysql.escape_string(d[0]), d[2]))


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
    data_0424 = [
        ['050008001032100', '35531'],  # 物理教科版八上
        ['050008002032100', '35545'],  # 物理教科版八下
        ['050009001032100', '35556'],  # 物理教科版九上
        ['050009002032100', '35567'],  # 物理教科版九下
    ]
    data_0424 = [
        # ['020001001005050', '25572'],  # 数学苏教版一上
        # ['020001002005050', '25573'],  # 数学苏教版一下
        # ['020002001005050', '25574'],  # 数学苏教版二上
        # ['020002002005050', '25575'],  # 数学苏教版二下
        ['020003001005050', '25576'],  # 数学苏教版三上
        ['020003002180217', '25577'],  # 数学苏教版三下
        ['020004001005050', '25578'],  # 数学苏教版四上
        ['020004002005050', '25579'],  # 数学苏教版四下
        ['020005001005050', '25580'],  # 数学苏教版五上
        ['020005002005050', '25581'],  # 数学苏教版五下
        ['020006001005050', '25582'],  # 数学苏教版六上
        ['020006002005050', '25592'],  # 数学苏教版六下

    ]
    result = []
    for data in data_0424:
        print(data)
        res = main(data[0], data[1])
        print(res)
        for r in res:
            result.append(r)
    print(result)
    print(len(result))
    print("\n\n")
    update_chapter(result)
