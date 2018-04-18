import os
import contextlib
import pymysql
import re
import requests


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


def valid_name(name):
    reg = re.compile(r'[\\/:*?".<>| \r\n]+')
    valid = reg.findall(name)
    if valid:
        for v in valid:
            name = name.replace(v, '')
    return name


def path_list(first):
    first_dir = 'F:/运营0417/{first}/'.format(first=first)
    seconds = os.listdir(first_dir)
    chapter = set()
    for second in seconds:
        chapter_path = first_dir + second
        resources = os.listdir(chapter_path)
        for res in resources:
            third_path = chapter_path + '/' + res
            if os.path.isdir(third_path):
                chapter.add(third_path)
            else:
                chapter.add(chapter_path)
    return chapter


def get_unit_id(chapter_id):
    with mysql() as cur:
        cur.execute("select unit_id from t_res_chapter where chapter_id = '{chapter_id}'".format(chapter_id=chapter_id))
        return cur.fetchone()


def cmp_str(str1, str2):
    if valid_name(str2) in valid_name(str1):
        return True
    return None


def modify_dir_name(book_id, dirs):
    with mysql() as cur:
        cur.execute(
            "select chapter_id,chapter_name from t_res_chapter where book_id = '{book_id}'".format(book_id=book_id))
        chapters = cur.fetchall()
        for dir in dirs:
            arr = dir.split('/')
            for c in chapters:
                if cmp_str(arr[-1], c.get('chapter_name')):  # 判断章节名是否相同
                    new_name = dir.replace(arr[-1], c.get('chapter_id'))
                    print(dir, new_name)
                    os.rename(dir, new_name)


support = ['png', 'jpg', 'mp3', 'mp4', 'flv', 'ppt', 'pptx', 'doc', 'docx', 'pdf']


def upload(book_id, path, subject_key, school_id, school_name, access_token):
    header = {'accessToken': access_token}
    data_list = []
    for c in path:
        res = os.listdir(c)
        chapter_id = c.split("/")[-1]
        unit_id = get_unit_id(chapter_id).get('unit_id')
        for r in res:
            if r[r.rindex('.') + 1:] in support:
                data_list.append("11")
                req = {
                    "currentSubject": subject_key,
                    "schoolId": school_id,
                    "schoolName": school_name,
                    "bookId": book_id,
                    "unitId": unit_id,
                    "chapterId": chapter_id,
                    "fileList": [
                        {
                            "fileName": r[:r.rindex(".")],
                            "fileType": r[r.rindex('.') + 1:],
                            "filePath": (c + '/' + r).replace('F:/运营', 'http://dfs.res.jzexueyun.com/resources/kx'),
                            "fileSize": os.path.getsize(c + '/' + r)
                        }
                    ]
                }
                # result = requests.post(url="http://api.cloudteach.jzexueyun.com/cloud/exueResource/uploadResource",
                #                        json=req, headers=header)
                # if result.status_code != 200:
                #     print(result.json())
                # else:
                #     print(result.status_code)
    print(len(data_list))


def main(book_id, subject_key, school_id, school_name, access_token):
    chapter = path_list(book_id)
    # modify_dir_name(book_id, chapter)
    upload(book_id, chapter, subject_key, school_id, school_name, access_token)


if __name__ == '__main__':
    subjectKey = 'kx'
    accessToken = '99f66c4c-bc16-4927-af4b-78e4c7893777'
    schoolId = "425741580347940864"
    schoolName = "资源研究中心"
    books = ['040003001066100', '040003002066100', '040004001066100', '040004002066100', '040005001066100',
             '040005002066100', '040006001066100', '040006002066100']
    # for b in books:
    #     main(book_id=b, subject_key=subjectKey, school_id=schoolId, school_name=schoolName, access_token=accessToken)
