import requests
from urllib.parse import urlencode

if __name__ == '__main__':
    data = {
        "gradeId":"G04",
        "courseId":"K01",
        "versionId":"V02",
        "volumeId":"1296"
    }
    resp = requests.post("http://www.jiaoxueyun.cn/resources-more-inter!getTrees.do?"+urlencode(data))
    print(resp.text)

    data = {
        "gradeId":"G04",
        "courseId":"K01",
        "versionId":"V16"
    }
    header = {
        "Cookie":"UM_distinctid=162467338a7c60-0a686962135185-3a61430c-1fa400-162467338a826e; JSESSIONID=7ECA2CCC96D9AD23A154FBBAB3982F31; JYY-Cookie-20480=EFLHKIMAFAAA; Hm_lvt_3b2b90b968014bee5b24ff51962ad7ac=1521600367,1521601043,1521775449; Hm_lvt_83bc962335f6e0741154dacdbf8c0c62=1521600367,1521601043,1521775449; name=value; Hm_lpvt_3b2b90b968014bee5b24ff51962ad7ac=1521775452; Hm_lpvt_83bc962335f6e0741154dacdbf8c0c62=1521775452; goa_page_pagesize_gotoPage=12; CNZZDATA1253279410=237130011-1521595576-http%253A%252F%252Fwww.jiaoxueyun.cn%252F%7C1521775472"
    }
    resp = requests.post(url="http://www.jiaoxueyun.cn/resources-more-inter!getVolumeAjaxs.do",data=data)
    print(resp.json())


