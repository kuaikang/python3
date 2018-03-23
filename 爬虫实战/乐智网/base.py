import requests, time, json
from selenium import webdriver
from urllib.parse import urlencode
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

header = {
    "Referer": "http://www.jiaoxueyun.cn/parent-resource!view.do?gradeId=G04&courseId=K01&versionId=V16&nodeIdSS=ff808081446180fa0144671311050003&flag=1",
    "Host": "www.jiaoxueyun.cn",
    "Connection": "keep-alive",
    "Origin": "http://www.jiaoxueyun.cn",
    "Content-Type": "application/json;charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    "Cookie": "JSESSIONID=2797A2053A9B5F756B52F29BE963892E; JYY-Cookie-20480=EFLHKIMAFAAA; name=value; UM_distinctid=1624e0ec632182-0c324f9f49603f-3a61430c-100200-1624e0ec6354af; CNZZDATA1253279410=1856900147-1521726488-http%253A%252F%252Fwww.jiaoxueyun.cn%252F%7C1521726488; goa_page_pagesize_gotoPage=12; wP_h=716e702abcf2ca100644575e712c0d5214902c22; Hm_lvt_3b2b90b968014bee5b24ff51962ad7ac=1521727889,1521728993; Hm_lpvt_3b2b90b968014bee5b24ff51962ad7ac=1521728993; Hm_lvt_83bc962335f6e0741154dacdbf8c0c62=1521727889,1521728993; Hm_lpvt_83bc962335f6e0741154dacdbf8c0c62=1521728993"
}


def get_grade():
    return {'G04': '一年级', 'G05': '二年级', 'G06': '三年级', 'G07': '四年级', 'G08': '五年级', 'G09': '六年级', 'G10': '七年级',
            'G11': '八年级', 'G12': '九年级', 'G13': '高一', 'G14': '高二', 'G15': '高三'}


def get_subject(grade_list):
    driver = webdriver.Chrome()
    driver.get("http://www.jiaoxueyun.cn/teacher-in!view.do")
    input(">>:")
    f = open("grade_subject.txt", mode="a", encoding="utf8")
    for grade in grade_list.keys():
        driver.find_element_by_id(grade).click()
        time.sleep(2)
        course_list = driver.find_element_by_id("courseList").find_elements_by_tag_name("a")
        d = {}
        for course in course_list:
            print(course.get_property("id"), course.text)
            d[course.get_property("id")] = course.text
        data = {grade: d}
        f.write(json.dumps(data, ensure_ascii=False))
        f.write("\n")
    f.close()
    driver.quit()


def get_version():
    driver = webdriver.Chrome()
    driver.get("http://www.jiaoxueyun.cn/teacher-in!view.do")
    input(">>:")
    f = open("grade_subject.txt", mode="r", encoding="utf8")
    f1 = open("version.txt", mode="a", encoding="utf8")
    for line in f.readlines():
        line = json.loads(line)
        for key in line.keys():
            driver.find_element_by_id(key).click()
            for s in line[key]:
                driver.find_element_by_id(s).click()
                time.sleep(3)
                version_list = driver.find_element_by_id("versionList").find_elements_by_tag_name("a")
                for version in version_list:
                    data = [key, s, version.get_property("id"), version.text]
                    f1.write(",".join(data))
                    f1.write("\n")
    f1.close()
    f.close()
    driver.quit()


def get_book():
    f = open("version.txt", mode="r", encoding="utf8")
    f_book = open("book.txt", mode="a", encoding="utf8")
    for line in f.readlines():
        line = line.strip().split(",")
        data = {
            "gradeId": line[0],
            "courseId": line[1],
            "versionId": line[2]
        }
        resp = requests.post(url="http://www.jiaoxueyun.cn/resources-more-inter!getVolumeAjaxs.do", data=data)
        for j in resp.json():
            if j:
                li = [line[0], line[1], line[2], j.get("courseListId"), j.get("courseListName")]
                f_book.write(",".join(li))
                f_book.write("\n")
        resp.close()
    f_book.close()
    f.close()


def get_chapter():
    f = open("book.txt", mode="r", encoding="utf8")
    for line in f.readlines():
        line = line.split(",")
        f_chapter = open("chapter_%s.txt" % line[0], mode="a", encoding="utf8")
        data = {
            "gradeId": line[0],
            "courseId": line[1],
            "versionId": line[2],
            "volumeId": line[3]
        }
        resp = requests.post("http://www.jiaoxueyun.cn/resources-more-inter!getTrees.do?" + urlencode(data))
        print(resp.json())
        f_chapter.close()
    f.close()


if __name__ == '__main__':
    get_chapter()
