import requests, re
from bs4 import BeautifulSoup
from urllib.parse import urlencode

head = {
    "Cookie": "isRemove=1; _ga=GA1.2.790539841.1520347247; Hm_lvt_6de0a5b2c05e49d1c850edca0c13051f=1520347420,1520422604,1520424925,1520854752; _gid=GA1.2.2125487473.1520854752; _csrf=05757b15d7d3295d79ce3f6145efdec8b91dc172a32d948c2d225b8ff739b9dba%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22GjexPG3UHDvwGSt9TpG8yOlFKa9VnNQp%22%3B%7D; isRemove=1; chid=27e8704a451201531cc9941f6f3b709b7e13397751c04b090603ffdb0a56dfb9a%3A2%3A%7Bi%3A0%3Bs%3A4%3A%22chid%22%3Bi%3A1%3Bs%3A1%3A%222%22%3B%7D; xd=ff8cc2c663e498cf1fffa3d89aaa8ae9f68a128de39a6036c46ec0a0ff0b9459a%3A2%3A%7Bi%3A0%3Bs%3A2%3A%22xd%22%3Bi%3A1%3Bs%3A1%3A%221%22%3B%7D; device=310bdaba05b30bb632f66fde9bf3e2b91ebc4d607c250c2e1a1d9e0dfb900f01a%3A2%3A%7Bi%3A0%3Bs%3A6%3A%22device%22%3Bi%3A1%3BN%3B%7D; _sync_login_identity=f7597f266cbbf231359e59aa50b1d0d0ea50e14b47cd76f17f21cfbb1efe30d3a%3A2%3A%7Bi%3A0%3Bs%3A20%3A%22_sync_login_identity%22%3Bi%3A1%3Bs%3A50%3A%22%5B1306170%2C%2245D9eP9ssO8LwbBEQz922cLDTGpI-B2a%22%2C86400%5D%22%3B%7D; PHPSESSID=bh50ib8uscjv0b42m3q8hst9g5; Hm_lpvt_6de0a5b2c05e49d1c850edca0c13051f=1520860930",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    "Accept-Encoding": "gzip, deflate"
}


# 查询教材
def teaching_material(xd, chid):
    url = "http://www.zujuan.com/question?chid=%s&xd=%s" % (chid, xd)
    resp = requests.get(url, headers=head)
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


def main():
    f = open("xx.txt", mode="a", encoding="utf8")
    for key in xx.keys():
        data = teaching_material("1", xx[key])
        for d in data:
            li = re.findall(pattern, d["href"])
            data = grades(li[0][0], 1, xx[key])
            for da in data:
                g = re.findall(pattern_grade, da["href"])[0]
                write_list = [key, xx[key], d["material"], li[0][0], da["grade_name"], g]
                f.write(",".join(write_list))
                f.write("\n")
    f.close()


if __name__ == '__main__':
    pattern = re.compile(".*?bookversion=(\d+)&chid=(\d)&xd=(\d).*?", re.S)
    pattern_grade = re.compile(".*?nianji=(\d+)&.*?", re.S)

    xx = {"语文": "2", "数学": "3", "英语": "3", "科学": "5", "政治思品": "9"}
    cz = {"语文": "2", "数学": "3", "英语": "4", "科学": "5", "物理": "6", "化学": "7", "历史": "8", "政治思品": "9",
          "历史与社会": "20", "生物": "11"}
    gz = {"语文": "2", "数学": "3", "英语": "3", "物理": "6", "化学": "7", "历史": "8", "政治思品": "9", "地理": "10", "生物": "11"}

    data = get_units("10902", "119480", "2", "1")
    data = requests.get("http://www.zujuan.com/question?categories=128314&bookversion=10902&nianji=128314&chid=2&xd=1", headers=head)
    print(data.text)
