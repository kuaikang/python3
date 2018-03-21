import requests

header = {
    "Cookie": "JSESSIONID=66DCFACA736EEA9B7D09170AC25ED004; Hm_lvt_83bc962335f6e0741154dacdbf8c0c62=1521601800; Hm_lvt_3b2b90b968014bee5b24ff51962ad7ac=1521601800; remPassord=true; loginName=13965127823; loginPwd=yj65127823; name=value; UM_distinctid=1624697799433-070bbbfe16eac6-3a61430c-1fa400-16246977995925; goa_page_pagesize_gotoPage=12; JYY-Cookie-20480=EFLHKIMAFAAA; CNZZDATA1253279410=1721267647-1521600982-http%253A%252F%252Fwww.educlouds.cn%252F%7C1521606397; Hm_lpvt_83bc962335f6e0741154dacdbf8c0c62=1521608376; Hm_lpvt_3b2b90b968014bee5b24ff51962ad7ac=1521608377",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
}
url_subject = "http://www.jiaoxueyun.cn/resources-more-inter!getCourse.do"
url_version = "http://www.educlouds.cn/resources-more-inter!getCourse.do"
url_book = "http://www.jiaoxueyun.cn/resources-more-inter!getVolumeAjaxs.do"


# 年级信息
def get_grade():
    return {'一年级': 'G04', '二年级': 'G05', '三年级': 'G06', '四年级': 'G07', '五年级': 'G08', '六年级': 'G09', '七年级': 'G10',
            '八年级': 'G11', '九年级': 'G12', '高一': 'G13', '高二': 'G14', '高三': 'G15'}


# 根据年级得到对应学科信息
def get_subject_by_grade(grade_id):
    req = {
        "gradeId": grade_id,
        "flag": "1",
        "courseId": "",
    }

    resp = requests.post(url=url_subject, data=req, headers=header)
    return resp.json().get("list")


# 根据年级和科目获得版本信息
def get_version(grade_id, subject_id):
    req = {
        "gradeId": grade_id,
        "flag": "2",
        "courseId": subject_id
    }
    print(req)
    resp = requests.post(url=url_version, headers=header, json=req)
    return resp.json()


def get_book(grade_id, subject_id, version_id):
    req = {
        "gradeId": grade_id,
        "versionId": version_id,
        "courseId": subject_id,
    }
    return requests.post(url=url_book, headers=header, json=req).json()


def write_grade_subject():  # 年级名称,年级id,课程名称,课程id,课本编号
    grade = get_grade()
    f = open("grade_subject.txt", mode="a", encoding="utf8")
    for key, val in grade.items():
        subjects = get_subject_by_grade(val)
        for sub in subjects:
            line = key, val, sub["courseName"], sub["courseId"], sub["courseNo"]
            print(",".join(line))
            f.write(",".join(line))
            f.write("\n")
    f.close()


if __name__ == '__main__':
    # write_grade_subject()
    pass