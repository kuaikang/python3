import requests
from bs4 import BeautifulSoup
import time

head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    "Cookie": "wP_h=716e702abcf2ca100644575e712c0d5214902c22; JSESSIONID=9C2B5299D522CD0A0BFCE046BBC41033; JYY-Cookie-20480=EGLHKIMAFAAA; Hm_lvt_83bc962335f6e0741154dacdbf8c0c62=1523280888; Hm_lvt_3b2b90b968014bee5b24ff51962ad7ac=1523280888; name=value; UM_distinctid=162aa9ec3d88e7-0d761b415d9b65-3a61430c-100200-162aa9ec3d96a9; CNZZDATA1253279410=587411053-1523277541-http%253A%252F%252Fwww.jiaoxueyun.cn%252F%7C1523277541; Hm_lpvt_3b2b90b968014bee5b24ff51962ad7ac=1523280957; Hm_lpvt_83bc962335f6e0741154dacdbf8c0c62=1523280957"
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
        time.sleep(0.8)
