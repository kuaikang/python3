import os
import contextlib
import pymysql
import re
import requests
import time


# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='123.206.227.74', port=3306, user='root', password='exue2017', db='topic_standard_test', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    finally:
        conn.commit()
        cur.close()
        conn.close()


# 格式化名称
def valid_name(name):
    reg = re.compile(r'[\\/:*?".<>| 《》◎：0123456789\r\n]+')
    valid = reg.findall(name)
    if valid:
        for v in valid:
            name = name.replace(v, '')
    return name


# 章节路径列表
def chapter_path(book_path):
    for index, ds, files in os.walk(book_path):
        return [os.path.join(index, d) for d in ds]


# 根据课本获取所有的章节信息,返回字典{"chapter_id":"unit_id"}
def get_unit(book_id):
    with mysql() as cur:
        cur.execute("SELECT * from t_res_chapter WHERE book_id = '{book_id}';".format(book_id=book_id))
        return {item.get('chapter_id'): item.get('unit_id') for item in cur.fetchall()}


# 根据课本获取所有的章节信息,返回字典{"chapter_id":"unit_id"}
def get_chapter(book_id):
    with mysql() as cur:
        cur.execute("SELECT * from t_res_chapter WHERE book_id = '{book_id}';".format(book_id=book_id))
        return cur.fetchall()


# 比对2个名称
def cmp_str(str1, str2):
    if valid_name(str1) in valid_name(str2):
        return True
    return False


# 修改章节名称为id,参数为课本路径
def modify_dir_name(path):
    book_id = os.path.split(path)[-1]
    chapters = get_chapter(book_id)
    chapter_dir = os.listdir(path)
    for chinese_name in chapter_dir:
        for c in chapters:
            print(c.get('chapter_name'))
            if cmp_str(chinese_name, c.get('chapter_name')):  # 判断章节名是否相同
                old_name = os.path.join(path, chinese_name)
                new_name = old_name.replace(chinese_name, c.get('chapter_id'))
                os.rename(old_name, new_name)
                chapters.remove(c)
                break


support = ['png', 'jpg', 'mp3', 'mp4', 'flv', 'ppt', 'pptx', 'doc', 'docx', 'pdf']


# 上传资源
def upload_resource(req, headers):
    result = requests.post(url="http://api.cloudteach.jzexueyun.com/cloud/exueResource/uploadResource",
                           json=req, headers=headers)
    if result.json().get('status') != 200:
        print(request)
        print(result.json())


def get_request(book_path, subject_key, req, headers):
    file_path = "http://dfs.res.jzexueyun.com/resources/{subject_key}/{unit_id}/{chapter_id}/{file_name}"
    book_id = os.path.split(book_path)[-1]
    chapter_dict = get_unit(book_id)
    c_path = chapter_path(book_path)
    for c in c_path:
        chapter_id = os.path.split(c)[-1]
        unit_id = chapter_dict.get(chapter_id)
        req['currentSubject'] = subject_key
        req['book_id'] = book_id
        req['unit_id'] = unit_id
        req['chapter_id'] = chapter_id
        res = os.listdir(c)
        for r in res:
            file_dict = {
                "fileName": r,
                "fileType": r[r.rindex(".") + 1:],
                "fileSize": os.path.getsize(os.path.join(c, r)),
                "filePath": file_path.format(subject_key=subject_key, unit_id=unit_id, chapter_id=chapter_id,
                                             file_name=r)
            }
            req['fileList'] = [file_dict]
            upload_resource(req, headers)


if __name__ == '__main__':
    header = {'accessToken': ""}
    request = {
        "schoolId": "425741580347940864",
        "schoolName": "资源研究中心"
    }
    books_yw = ['010002002154194']  # 语文
    books_dd = ['240007002446350', '240008001116653']  # 道德与法治
    books_sp = ['160009001045100']  # 思想品德
    # for book_id in books_sp:
    #     modify_dir_name("F:/运营0423/{book_id}".format(book_id=book_id))
    # for book_id in books:
    # get_request("F:/运营0423/{book_id}".format(book_id=book_id), "yw", request, header)

    # 打印资源路径
    # for item in chapter_path("F:/运营0423/160009001045100"):
    #     data = os.listdir(item)
    #     for d in data:
    #         print(os.path.join(item,d))
