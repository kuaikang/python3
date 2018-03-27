import requests
import os
import pymysql


def get_db_res():
    # 打开数据库连接
    db = pymysql.connect(
        host="123.206.227.74", user="root",
        password="exue2017", db="topic_standard_test", port=3306,
        charset="utf8"
    )
    return db


def path_dir(subject_key):
    path = "E:\\resource\\%s" % subject_key
    grades = os.listdir(path)
    result = []
    for grade in grades:
        grade_path = os.path.join(path, grade)
        versions = os.listdir(grade_path)
        for version in versions:
            version_path = os.path.join(grade_path, version)
            books = os.listdir(version_path)
            for book in books:
                if not book.split('_')[-1].isdigit(): continue
                book_path = os.path.join(version_path, book)
                chapters = os.listdir(book_path)
                for chapter in chapters:
                    res_path = os.path.join(book_path, chapter)
                    res = os.listdir(res_path)
                    for r in res:
                        li = [book.split('_')[-1], chapter.split('_')[-1], os.path.join(res_path, r), r[:r.rfind('.')]]
                        result.append(li)
    return result


# 修改章节名称(课本id,课本目录)
def modify_chapter(book_id, path):
    db = get_db_res()
    cur = db.cursor()
    cur.execute("select chapter_id,chapter_name from t_res_chapter where book_id = '%s'" % book_id)
    chapter_ids = cur.fetchall()
    chapters = os.listdir(path)
    for c in chapter_ids:
        print(c)
        for f in chapters:
            if f in c[1]:
                old_name = os.path.join(path, f)
                new_name = os.path.join(path, '_'.join([c[1].replace('*', ' '), c[0]]))
                os.rename(old_name, new_name)


def get_unit_id(cur, chapter_id):
    cur.execute("select unit_id from t_res_chapter where chapter_id = '%s'" % chapter_id)
    unit = cur.fetchone()
    return unit[0]


def main(subject_key, upload_url, upload_resource_url, schoolId, schoolName, accessToken):
    db = get_db_res()
    cur = db.cursor()
    data = path_dir(subject_key)
    for d in data:
        unit_id = get_unit_id(cur, d[1])
        if os.path.getsize(d[2]) / 1024 / 1024 >= 1: continue
        with open(d[2], mode="rb") as f:
            resp = requests.post(url=upload_url, files={"file": f})
            data = resp.json()
            if data.get('status') != 200: continue
            req = {
                "currentSubject": subject_key,
                "schoolId": schoolId,
                "schoolName": schoolName,
                "bookId": d[0],
                "unitId": unit_id,
                "chapterId": d[1],
                "fileList": [
                    {
                        "fileName": d[-1],
                        "fileType": data.get('content').get('fileType'),
                        "filePath": data.get('content').get('accessUrl'),
                        "fileSize": data.get('content').get('fileSize')
                    }
                ]
            }
            header = {'accessToken': accessToken}
            requests.post(url=upload_resource_url, json=req,
                          headers=header)
            print(req)
    cur.close()
    db.close()


if __name__ == '__main__':
    # modify_chapter('100009002056100', 'E:\\resource\\ls\\九年级\\北师大版\\下册_100009002056100')

    subject_key = 'sx'
    schoolId = "425741580347940864",
    schoolName = "资源研究中心"
    accessToken = '4af2386a-43be-4879-b579-c68ea142b7ce'
    upload_url = "http://dfs.upload1.jzexueyun.com/cos/upload"
    upload_resource_url = 'http://api.cloudteach.jzexueyun.com/cloud/exueResource/uploadResource'
    # main(subject_key=subject_key, upload_url=upload_url, upload_resource_url=upload_resource_url, schoolId=schoolId,
    #      schoolName=schoolName, accessToken=accessToken)

    with open('E:\\resource\\sx\\七年级\\北师大版\\下册_020007002006048\\2.4 用尺规作角_020007002006048002004\\用尺规作角 课件1.ppt',
              mode="rb") as f:
        resp = requests.post(url=upload_url, files={'file': f})
        print(resp.text)
