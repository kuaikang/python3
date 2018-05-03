import requests
from common.request_util import headers
from bs4 import BeautifulSoup
import json
from common.excel_util import create_excel

grade = {
    "一年级": "grade_11",
    "二年级": "grade_12",
    "三年级": "grade_13",
    "四年级": "grade_14",
    "五年级": "grade_15",
    "六年级": "grade_16",
    "初一": "grade_2",
    "初二": "grade_3",
    "初三": "grade_4",
    "高一": "grade_5",
    "高二": "grade_6",
    "高三": "grade_7",
}

grade_dict = {"grade_11": "一年级", "grade_12": "二年级", "grade_13": "三年级", "grade_14": "四年级", "grade_15": "五年级",
              "grade_16": "六年级", "grade_2": "初一", "grade_3": "初二", "grade_4": "初三", "grade_5": "高一", "grade_6": "高二",
              "grade_7": "高三"}

base_url = "http://zhibo.zuoyebang.com"
get_subject_url = "http://zhibo.zuoyebang.com/goods/web/course/list?type={type}&grade={grade}"
get_season_url = "http://zhibo.zuoyebang.com/goods/web/course/list?type={type}&grade={grade}&subject={subject}"
get_resource_url = "http://zhibo.zuoyebang.com/goods/web/course/list?type={type}&grade={grade}&subject={subject}" \
                   "&season={season}&rn=9&pn={pn}"


def get_subject(grade):
    resp = requests.get(url=get_subject_url.format(type='0', grade=grade), headers=headers)
    soup = BeautifulSoup(resp.content.decode(), "lxml")
    data = soup.find(attrs={"class": "subject"}).select('li')
    return {item['data-subject']: item.text for item in data if item.text != '科目：' and item.text != '全部'}


def parse_subject():
    f = open("subject.txt", mode="w", encoding="utf8")
    for key, val in grade.items():
        dic = get_subject(val.split('_')[-1])
        f.write(json.dumps({val: dic}, ensure_ascii=False))
        f.write("\n")
    f.close()


def get_season(grade, subject):
    resp = requests.get(url=get_season_url.format(type='2', grade=grade, subject=subject), headers=headers)
    soup = BeautifulSoup(resp.content.decode(), "lxml")
    data = soup.find(attrs={"class": "season"}).select('li')
    return {item['data-season']: item.text for item in data if item.text != '学期：' and item.text != '全部'}


def parse_season():
    f_write = open("season.txt", mode="w", encoding="utf8")
    with open("subject.txt", mode="r", encoding="utf8") as f:
        for line in f.readlines():
            line = json.loads(line.strip())
            for key, val in line.items():
                for s_id, s_name in val.items():
                    data = get_season(key, s_id)
                    print(data)
                    f_write.write(json.dumps({"grade": key, "subject": s_id, "subject_name": s_name, "data": data},
                                             ensure_ascii=False))
                    f_write.write("\n")
    f_write.close()


def get_info_url(grade_id, subject, season=None, pn=0):
    resp = requests.get(url=get_resource_url.format(type='0', grade=grade_id, subject=subject, season=season, pn=pn),
                        headers=headers)
    soup = BeautifulSoup(resp.content.decode(), "lxml")
    data = soup.find_all(attrs={"class": "course-link"})
    if data:
        return [item['href'] for item in data]
    return None


def get_info(url):
    """课程名,时间,适合,老师,原价,现价,报名信息"""
    resp = requests.get(url=base_url + url, headers=headers)
    soup = BeautifulSoup(resp.content.decode(), "lxml")
    base_info = soup.find(attrs={"class": "course-baseinfo"})
    keys = ['course-name', 'time', 'fit', 'name']
    result = [base_info.find(attrs={"class": key}).text for key in keys]
    ext_info = soup.find(attrs={"class": "course-extinfo"})
    if ext_info:
        price_info = ext_info.find(attrs={"class": "price"})
        if price_info.get('original'):
            result.append(price_info.get('original'))
        else:
            result.append(price_info.text)
        result.append(price_info.text)
        sign_up = ext_info.find(attrs={"class": "timer enroll-info"})
        if sign_up:
            result.append(sign_up.get('enroll-cnt'))
    return result


def main():
    result = [['课程名', '时间', '教版版本', '老师', '原价', '现价', '报名信息', '年级', '学科']]
    f_read = open("season.txt", mode="r", encoding="utf8")
    for line in f_read.readlines():
        line = json.loads(line.strip())
        data = line.get('data')
        for key, val in data.items():
            pn = 0
            while True:
                url_list = get_info_url(line.get('grade'), line.get('subject'), key, pn=pn)
                if not url_list: break
                for u in url_list:
                    info = get_info(u)
                    info.append(grade_dict['grade_' + line.get('grade')])
                    info.append(line.get('subject_name'))
                    result.append(info)
                    print(info)
                pn += 9
    f_read.close()
    create_excel(result, "F:/作业帮_长期班.xlsx")


def main_interesting():
    result = [['课程名', '时间', '教版版本', '老师', '原价', '现价', '报名信息', '年级', '学科']]
    f_read = open("subject_interesting.txt", mode="r", encoding="utf8")
    for line in f_read.readlines():
        line = json.loads(line.strip())
        for key, val in line.items():
            for k in val.keys():
                pn = 0
                while True:
                    url_list = get_info_url(key.split('_')[-1], k, pn=pn)
                    if not url_list: break
                    for u in url_list:
                        info = get_info(u)
                        info.append(grade_dict[key])
                        info.append(val.get(k))
                        result.append(info)
                        print(info)
                    pn += 9
    f_read.close()
    create_excel(result, "F:/作业帮_专题课.xlsx")


if __name__ == '__main__':
    main_interesting()
