import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import re, json

resoucr_url = "http://www.jiaoxueyun.cn/resources-more!getTeachingResource.do?"
pattern_resoucr_id = re.compile(".*?resource_id=(.*?)&.*?", re.S)


def get_resource_id(grade_id, version_id, course_id, node_id, extension_name):
    data = {
        "type": "T01,",
        "gradeId": grade_id,
        "versionId": version_id,
        "courseId": course_id,
        "nodeId": node_id,
        "extension_name": extension_name
    }
    f = open("resource/res_%s.txt" % grade_id, mode="a", encoding="utf8")
    resp = requests.get(url=resoucr_url + urlencode(data))
    soup = BeautifulSoup(resp.text, "lxml")
    tds = soup.find_all(attrs={"style": "font-weight: bold;cursor: pointer;"})
    if not tds:
        return
    for td in tds:
        resource_id = re.findall(pattern_resoucr_id, td["onclick"])[0]
        dic = {node_id: {resource_id: td["title"]}}
        print(dic)
        f.write(json.dumps(dic, ensure_ascii=False))
        f.write("\n")
    f.close()


if __name__ == '__main__':
    # head = {
    #     "Cookie": "UM_distinctid=162467338a7c60-0a686962135185-3a61430c-1fa400-162467338a826e; Hm_lvt_3b2b90b968014bee5b24ff51962ad7ac=1521600367,1521601043,1521775449; Hm_lvt_83bc962335f6e0741154dacdbf8c0c62=1521600367,1521601043,1521775449; name=value; goa_page_pagesize_gotoPage=12; JYY-Cookie-20480=EFLHKIMAFAAA; JSESSIONID=C93258D9ABFCB3D932633AC06E0473BB; remPassord_=true; userName=13965127823; userPassword=yj65127823; CNZZDATA1253279410=237130011-1521595576-http%253A%252F%252Fwww.jiaoxueyun.cn%252F%7C1521791682; Hm_lpvt_83bc962335f6e0741154dacdbf8c0c62=1521792981; Hm_lpvt_3b2b90b968014bee5b24ff51962ad7ac=1521792981"
    # }
    # url = "http://www.jiaoxueyun.cn/res-view!download.do?resource_id=8a92916a4327be5401432c81eeb66e5e"
    # resp = requests.get(url=url, headers=head)
    # if '登录' not in resp.text:
    #     f = open("doc/1.doc", mode="ab")
    #     f.write(resp.content)
    #     f.close()
    f_book = open("book.txt", mode="r", encoding="utf8")  # G04,K01,V16,ff808081446180fa0144671311050003,上册
    book = f_book.readlines()
    f_book.close()
    f = open("chapter/chapter_G10.txt", mode="r", encoding="utf8")
    for line in f.readlines():
        line = line.split(",")
        # line[2] node_id
        for b in book:
            if line[0] in b and "G10" in b:
                b = b.split(",")
                get_resource_id(b[0], b[2], b[1], line[2], "DOC")
    f.close()
