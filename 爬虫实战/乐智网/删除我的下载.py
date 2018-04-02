import requests
from bs4 import BeautifulSoup
import time

head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    "Cookie": "UM_distinctid=1624e0ec632182-0c324f9f49603f-3a61430c-100200-1624e0ec6354af; remPassord_=true; userName=13965127823; userPassword=yj65127823; remPassord=true; loginName=13965127823; loginPwd=yj65127823; JSESSIONID=F809177DA56A268A0AF5513B2E02E57E; JYY-Cookie-20480=EELHKIMAFAAA; Hm_lvt_83bc962335f6e0741154dacdbf8c0c62=1522334113,1522505080,1522545748,1522674120; Hm_lvt_3b2b90b968014bee5b24ff51962ad7ac=1522334113,1522505080,1522545748,1522674120; name=value; CNZZDATA1253279410=1856900147-1521726488-http%253A%252F%252Fwww.jiaoxueyun.cn%252F%7C1522673513; goa_page_pagesize_gotoPage=12; Hm_lpvt_83bc962335f6e0741154dacdbf8c0c62=1522674134; Hm_lpvt_3b2b90b968014bee5b24ff51962ad7ac=1522674135"
}


def main():
    resp = requests.post("http://www.jiaoxueyun.cn/personal!download.do", headers=head)
    soup = BeautifulSoup(resp.text, "lxml")
    table = soup.find(attrs={"class": "table2"})
    trs = table.select('tr')
    if not trs: return
    for tr in trs:
        temp = tr.select("img")[-1]["onclick"]
        del_id = temp[temp.index("'") + 1:temp.rindex("'")]
        print(del_id)
        requests.post("http://www.jiaoxueyun.cn/personal!deleteDownload.do", data={"key": del_id}, headers=head)


if __name__ == '__main__':
    print("定时清除我的下载")
    while True:
        main()
        time.sleep(1)
