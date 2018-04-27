import requests
from urllib.parse import urlencode
import json
import time
from common.excel_util import create_excel

grade = [
    {"studyPhase": "xiaoxue", "grade": "100", "grade_name": "幼升小"},
    {"studyPhase": "xiaoxue", "grade": "1", "grade_name": "一年级"},
    {"studyPhase": "xiaoxue", "grade": "2", "grade_name": "二年级"},
    {"studyPhase": "xiaoxue", "grade": "3", "grade_name": "三年级"},
    {"studyPhase": "xiaoxue", "grade": "4", "grade_name": "四年级"},
    {"studyPhase": "xiaoxue", "grade": "5", "grade_name": "五年级"},
    {"studyPhase": "xiaoxue", "grade": "6", "grade_name": "六年级"},
    {"studyPhase": "chuzhong", "grade": "7", "grade_name": "七年级"},
    {"studyPhase": "chuzhong", "grade": "8", "grade_name": "八年级"},
    {"studyPhase": "chuzhong", "grade": "9", "grade_name": "九年级"},
    {"studyPhase": "gaozhong", "grade": "10", "grade_name": "高一"},
    {"studyPhase": "gaozhong", "grade": "11", "grade_name": "高二"},
    {"studyPhase": "gaozhong", "grade": "12", "grade_name": "高三"}
]

headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
}
subject_url = "https://www.yuanfudao.com/tutor-student-lesson/api/channels/all?"
course_url = "https://www.yuanfudao.com/tutor-student-lesson/api/homepage?"


def get_subject(studyPhase, gradeId):
    data = {
        "studyPhase": studyPhase,
        "gradeId": gradeId,
        "withNextGrade": "false",
        "platform": "www",
        "version": "5.11.0",
        "UDID": "e7dd01c28a9f5177a0004553a2a827d9",
        "timestamp": "1524807110010"
    }
    resp = requests.get(subject_url + urlencode(data), headers=headers)
    return resp.json()


def parse_subject():
    f = open("subject.txt", mode="a", encoding="utf8")
    for g in grade:
        data = get_subject(g['studyPhase'], g['grade'])
        for item in data:
            item['studyPhase'] = g['studyPhase']
            item['grade'] = g['grade']
            f.write(json.dumps(item, ensure_ascii=False))
            f.write("\n")
            print(item)
    f.close()


def get_course(studyPhase, gradeId, channelId):
    data = {
        "studyPhase": studyPhase,
        "grade": gradeId,
        "channelId": channelId,
        "startCursor": "0",
        "limit": "18",
        "withNextGrade": "false",
        "platform": "www",
        "version": "5.11.0",
        "UDID": "e7dd01c28a9f5177a0004553a2a827d9",
        "timestamp": "1524807110010"
    }
    resp = requests.get(course_url + urlencode(data), headers=headers)
    return resp.json()


def parse_course():
    with open("subject.txt", mode="r", encoding="utf8") as f:
        f_write = open("course_info.txt", mode="a", encoding="utf8")
        for line in f.readlines():
            line = json.loads(line.strip())
            data = get_course(line.get('studyPhase'), line.get('grade'), line.get('id'))
            if data:
                dic = {"grade": line.get('grade'), "name": line.get('name'), "data": data}
                f_write.write(json.dumps(dic, ensure_ascii=False))
                f_write.write("\n")
            time.sleep(1)
        f_write.close()


def save_excel(out_file):
    with open("course_info.txt", mode="r", encoding="utf8") as f:
        result = [['年级', '科目', '类型', '课程名', '开课时间', '老师', '价格', '报名人数']]
        for line in f.readlines():
            line = json.loads(line.strip())
            data = line.get('data')
            data_list = data.get('list')
            for item in data_list:
                if line.get('name') == '全部': continue
                if line.get('grade') == '100': continue
                res = [line.get('grade'), line.get('name')]
                if item.get('label'):
                    res.append(item.get('label'))
                else:
                    res.append("讲座")
                res.append(item.get('name'))  # 课程名
                res.append(item.get('subName'))  # 开课时间
                res.append(",".join([it.get('nickname') for it in item.get('teachers')]))
                if item.get('minPrice'):
                    res.append(item.get('minPrice'))
                else:
                    res.append(item.get('product').get('price'))
                res.append(item.get('product').get('soldCount'))
                result.append(res)
        create_excel(result, out_file)


if __name__ == '__main__':
    # print(get_course("chuzhong", "8", "2"))
    # parse_course()
    save_excel(out_file="F:/yuanfudao.xlsx")
