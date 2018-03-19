import requests,re
from bs4 import BeautifulSoup

if __name__ == '__main__':
    head={
        "Cookie":"isRemove=1; _ga=GA1.2.1209185538.1520329414; _gid=GA1.2.1039098456.1521423702; PHPSESSID=lqh5c7ns81btc3fb1rrj8d26o4; _csrf=81bcf7fd71f377cb62c695f2f8d9b72ac359c7455ad6c524c154cb35b44b2446a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22BNYTnqAqjJvpjtaM3PdDHYWVOORLG3I9%22%3B%7D; isRemove=1; Hm_lvt_6de0a5b2c05e49d1c850edca0c13051f=1521177189,1521423696,1521423702,1521446251; chid=27e8704a451201531cc9941f6f3b709b7e13397751c04b090603ffdb0a56dfb9a%3A2%3A%7Bi%3A0%3Bs%3A4%3A%22chid%22%3Bi%3A1%3Bs%3A1%3A%222%22%3B%7D; xd=ff8cc2c663e498cf1fffa3d89aaa8ae9f68a128de39a6036c46ec0a0ff0b9459a%3A2%3A%7Bi%3A0%3Bs%3A2%3A%22xd%22%3Bi%3A1%3Bs%3A1%3A%221%22%3B%7D; Hm_lpvt_6de0a5b2c05e49d1c850edca0c13051f=1521446435"
    }
    resp = requests.get("http://www.zujuan.com/question/detail-6909479.shtml",headers=head)
    soup = BeautifulSoup(resp.text,"lxml")
    pattern = re.compile('.*?"answer":"(.*?)>*?"',re.S)
    script = soup.find(attrs={"src":"/site/get-parameters"})
    print(re.findall(pattern,resp.text))
    resp.close()