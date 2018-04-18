import requests
from bs4 import BeautifulSoup
import time

head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    "Cookie":"UM_distinctid=162467338a7c60-0a686962135185-3a61430c-1fa400-162467338a826e; remPassord_=true; userName=13965127823; userPassword=yj65127823; remPassord=true; loginName=13965127823; loginPwd=yj65127823; Hm_lvt_83bc962335f6e0741154dacdbf8c0c62=1523256735,1523959116; Hm_lvt_3b2b90b968014bee5b24ff51962ad7ac=1523256735,1523959116; name=value; goa_page_pagesize_gotoPage=12; JYY-Cookie-20480=EELHKIMAFAAA; JSESSIONID=8279553F4B33F2A6A0A985097B38E833; CNZZDATA1253279410=1838872367-1523255924-http%253A%252F%252Fwww.jiaoxueyun.cn%252F%7C1524011692; Hm_lpvt_3b2b90b968014bee5b24ff51962ad7ac=1524014370; Hm_lpvt_83bc962335f6e0741154dacdbf8c0c62=1524014370"
}


def main():
    resp = requests.post("http://www.jiaoxueyun.cn/personal!download.do", headers=head)
    soup = BeautifulSoup(resp.text, "lxml")
    table = soup.find(attrs={"class": "table2"})
    trs = table.select('tr')
    resp.close()
    if not trs: return
    for tr in trs:
        temp = tr.select("img")[-1]["onclick"]
        del_id = temp[temp.index("'") + 1:temp.rindex("'")]
        print(del_id)
        try:
            requests.post("http://www.jiaoxueyun.cn/personal!deleteDownload.do", data={"key": del_id}, headers=head)
        except Exception:
            continue


if __name__ == '__main__':
    print("定时清除我的下载")
    while True:
        main()
        time.sleep(2)
