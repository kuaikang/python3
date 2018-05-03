import requests
from common.request_util import headers
from bs4 import BeautifulSoup
import json
from common.excel_util import create_excel


def get_grade():
    f_write = open("grade.txt", mode="w", encoding="utf8")
    resp = requests.get(url="https://fudao.qq.com/?grade=7001", headers=headers)
    soup = BeautifulSoup(resp.text, "lxml")
    grade_list = soup.find(attrs={"class": "grade-area"}).select('a')
    for item in grade_list:
        if item.get('data-ext1'):
            print(item.get('data-ext1'), item.text)
            f_write.write(json.dumps({item.get('data-ext1'): item.text}, ensure_ascii=False))
            f_write.write("\n")
    f_write.close()


def get_subject(grade):
    data = {}
    resp = requests.get(url="https://fudao.qq.com/?grade=%s" % grade, headers=headers)
    soup = BeautifulSoup(resp.text, "lxml")
    subject_list = soup.find(attrs={"class": "subject-list"}).select('li')
    for item in subject_list:
        if item.select('a')[-1].get('class')[0] == 'disabled': continue
        if item.get('data-ext1'):
            data[item.get('data-ext1')] = item.text
    return data


grade_dict = {'7001': '一年级', '7002': '二年级', '7003': '三年级', '7004': '四年级', '7005': '五年级', '7006': '六年级', '6001': '初一',
              '6002': '初二', '6003': '初三', '5001': '高一', '5002': '高二', '5003': '高三'}


def subject_write():
    f_write = open("subject.txt", mode="w", encoding="utf8")
    for key, val in grade_dict.items():
        info = get_subject(key)
        if info:
            f_write.write(json.dumps({key: info}, ensure_ascii=False))
            f_write.write("\n")
    f_write.close()


def get_info(grade, subject):
    resp = requests.get(
        url="https://fudao.qq.com/?grade={grade}&subject={subject}".format(grade=grade, subject=subject),
        headers=headers)
    soup = BeautifulSoup(resp.text, "lxml")
    keys = ['item-title', 'item-course-info', 'teacher-name', '__price', '__sold']
    course_list = soup.find(attrs={"class": "course-list"}).select('li')
    result = []
    for item in course_list:
        data = []
        for key in keys:
            data.append(item.find(attrs={"class": key}).text)
        result.append(data)
    return result


def main():
    result = [['年级', '学科', '课程名', '时间', '老师', '价格', '报名状态']]
    f_read = open("subject.txt", mode="r", encoding="utf8")
    for line in f_read.readlines():
        line = json.loads(line.strip())
        for key, val in line.items():
            for k, v in val.items():
                data = get_info(key, k)
                for d in data:
                    res = [grade_dict[key], v]
                    res.extend(d)
                    result.append(res)
                    print(res)
    f_read.close()
    create_excel(result, "F:/企鹅辅导.xlsx")


if __name__ == '__main__':
    main()
