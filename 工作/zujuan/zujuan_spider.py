import requests, re, threading,time
from bs4 import BeautifulSoup
from urllib.parse import urlencode

head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Cookie": "_ga=GA1.2.1209185538.1520329414; PHPSESSID=6remccd1kkj5u9dpr0hrge6d55; _csrf=8685cce2e855a0a52089f8b5c0a217deca8611ea1b42bed9f8b165e78903d6e0a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22QYj_EGq8yvTeM5M1H7PXj7QVVy-CIAt-%22%3B%7D; isRemove=1; _gid=GA1.2.2094392116.1520841879; chid=27e8704a451201531cc9941f6f3b709b7e13397751c04b090603ffdb0a56dfb9a%3A2%3A%7Bi%3A0%3Bs%3A4%3A%22chid%22%3Bi%3A1%3Bs%3A1%3A%222%22%3B%7D; xd=ff8cc2c663e498cf1fffa3d89aaa8ae9f68a128de39a6036c46ec0a0ff0b9459a%3A2%3A%7Bi%3A0%3Bs%3A2%3A%22xd%22%3Bi%3A1%3Bs%3A1%3A%221%22%3B%7D; Hm_lvt_6de0a5b2c05e49d1c850edca0c13051f=1520329414,1520841881,1520917709; _gat_gtag_UA_112991577_1=1; Hm_lpvt_6de0a5b2c05e49d1c850edca0c13051f=1520918318"
}


# 查询教材
def teaching_material(xd, chid):
    url = "http://www.zujuan.com/question?"
    req = {"chid": chid, "xd": xd}
    resp = requests.get(url + urlencode(req), headers=head)
    soup = BeautifulSoup(resp.text, "lxml")
    data = soup.find_all(attrs={"class": "con-items"})[0].select('a')
    for index in data:
        yield {
            "href": url + index.attrs['href'],
            "material": index.get_text()
        }
    return data


def grades(bookversion, xd, chid):  # 年级
    url = "http://www.zujuan.com/question?bookversion=%s&chid=%s&xd=%s" % (bookversion, chid, xd)
    resp = requests.get(url, headers=head)
    soup = BeautifulSoup(resp.text, "lxml")
    data = soup.find_all(attrs={"class": "con-items"})[1].select('a')
    for index in data:
        yield {
            "href": "http://www.zujuan.com" + index.attrs['href'],
            "grade_name": index.get_text()
        }
    return data


def get_units(bookversion, nianji, chid, xd):
    url = "http://www.zujuan.com/question?"
    req = {"categories": nianji, "nianji": nianji, "bookversion": bookversion, "chid": chid, "xd": xd}
    resp = requests.get(url + urlencode(req), headers=head)
    soup = BeautifulSoup(resp.text, "lxml")
    data = soup.find(attrs={"id": "J_Tree"}).select('a')
    return resp
    # ids = soup.find(attrs={"id": "J_Tree"})
    # return [x.get_text() for x in data], ids


def main(pattern, pattern_grade, xx, file_name, level):
    f = open(file_name, mode="a", encoding="utf8")
    for key in xx.keys():
        data = teaching_material(level, xx[key])
        for d in data:
            li = re.findall(pattern, d["href"])
            data = grades(li[0][0], level, xx[key])
            for da in data:
                g = re.findall(pattern_grade, da["href"])[0]
                write_list = [key, xx[key], d["material"], li[0][0], da["grade_name"], g]
                f.write(",".join(write_list))
                f.write("\n")
            time.sleep(0.3)
    f.close()


if __name__ == '__main__':
    pattern = re.compile(".*?bookversion=(\d+)&chid=(\d)&xd=(\d).*?", re.S)
    pattern_grade = re.compile(".*?nianji=(\d+)&.*?", re.S)

    xx = {"语文": "2", "数学": "3", "英语": "4", "科学": "5", "政治思品": "9"}
    cz = {"语文": "2", "数学": "3", "英语": "4", "科学": "5", "物理": "6", "化学": "7", "历史": "8", "政治思品": "9",
          "历史与社会": "20", "生物": "11"}
    gz = {"语文": "2", "数学": "3", "英语": "4", "物理": "6", "化学": "7", "历史": "8", "政治思品": "9", "地理": "10", "生物": "11"}

    t1 = threading.Thread(target=main, args=(pattern, pattern_grade, xx, "xx.txt", "1",))
    t1.start()