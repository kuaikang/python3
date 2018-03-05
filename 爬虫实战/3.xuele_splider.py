import requests, json, time, threading, os
from 文档操作.excel import excel_util

request_headers = {
    "cookie": "SESSION=ACC792C81A48826542EDD58F22825786; LOGOTIPS=1",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}


def get_subject():
    urls = "http://www.xueleyun.com/member/book/selectSubjectBySchool.ajax"
    request_data = {"schoolId": "10001"}
    resp = requests.post(url=urls, data=request_data, headers=request_headers)
    return resp.content.decode()


def get_grade():
    request_url = "http://www.xueleyun.com/member/book/selectSchoolGrade.ajax"
    request_data = {"schoolId": "10001"}
    resp = requests.post(url=request_url, data=request_data, headers=request_headers)
    return resp.json()


def get_editions(grade, subject_id):
    request_url = "http://www.xueleyun.com/member/book/selectEditionBySubject.ajax"
    request_data = {"grade": grade, "subjectId": subject_id}
    resp = requests.post(url=request_url, data=request_data, headers=request_headers)
    return resp.content.decode()


def get_books(grade, edition, subject):
    request_url = "http://www.xueleyun.com/member/book/selectBooksBySubjectGradeEdition.ajax"
    request_data = {"gradeCode": grade, "editionId": edition, "subjectId": subject}
    resp = requests.post(url=request_url, data=request_data, headers=request_headers)
    return resp.content.decode()


def task(summary_code, summary_name, grades):
    f = open("%s.txt" % summary_code, mode="a", encoding="utf8")
    for grade in grades.get("wrapper"):
        res = get_editions(grade, summary_code)
        res = json.loads(res)
        for dic in res.get("wrapper"):
            resp = get_books(grade, dic["editionId"], summary_code)
            resp = json.loads(resp)
            dic.pop("editionId")
            for li in resp.get("wrapper"):
                dic["bookName"] = li["bookName"]
                dic["summaryName"] = summary_name
                dic["grade"] = str(grade)
                f.write(json.dumps(dic, ensure_ascii=False))
                f.write("\n")
                time.sleep(0.1)
    f.close()


def main():
    try:
        res_subjects = get_subject()
        grades = get_grade()
        res_subjects = json.loads(res_subjects)
        threads = []
        for subject in res_subjects.get("wrapper"):
            t = threading.Thread(target=task, args=(subject["summaryCode"], subject["summaryName"], grades,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    except Exception:
        print("error")


def merge_file(file_name):
    res_subjects = get_subject()
    grades = get_grade()
    res_subjects = json.loads(res_subjects)
    file = open(file_name, mode="a", encoding="utf8")
    for subject in res_subjects.get("wrapper"):
        f = open("%s.txt" % subject["summaryCode"], mode="r", encoding="utf8")
        file.write(f.read())
        f.close()
        os.remove("%s.txt" % subject["summaryCode"])
    file.close()


def generator_excel(file_name):
    # 读取txt中的字典,生成excel
    data_list = [["出版社", "版本", "教材", "科目", "年级"]]
    f = open(file_name, mode="r", encoding="utf8")
    for line in f.readlines():
        line = json.loads(line)
        li = []
        for val in line.values():
            li.append(val)
        data_list.append(li)
    f.close()
    os.remove(file_name)
    excel_util.create_excel(data_list)


if __name__ == '__main__':
    main()
    file_name = "all.txt"
    merge_file(file_name)
    generator_excel(file_name)
    print("finish")
