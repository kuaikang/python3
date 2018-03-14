import requests, json, re
from bs4 import BeautifulSoup

cz_dic = {"2": "语文", "3": "数学", "4": "英语", "6": "物理", "7": "化学", "8": "历史", "9": "政治思品", "10": "地理", "11": "生物"}


# 获取出版版本
def get_version(xd, channel):
    resp = requests.get("http://tiku.21cnjy.com/tiku.php?mod=quest&channel=%s&xd=%s" % (channel, xd))
    soup = BeautifulSoup(resp.text, "lxml")
    data = soup.find_all(attrs={"class": "hasChildren"})
    result = []
    for item in data:  # item["id"] 版本id  item.get_text().strip() 版本名 item.select("a")[0]["href"] 路径
        it = [cz_dic[channel], channel, item.get_text().strip(), item["id"]]
        result.append(it)
    return result


# 获取书本
def get_book(version_id):
    req = {"root": version_id, "op": "ajaxcatid", "additional": "yeah: Tue, 13 Mar 2018 15:21:17 GMT"}
    resp = requests.post(url="http://tiku.21cnjy.com/tiku.php?mod=quest", data=req)
    if len(resp.json()) == 0:
        return None
    pattern_book = re.compile('.*?catid=(\d+)">(.*?)<.*?', re.S)
    result = []
    for it in resp.json():
        d = re.findall(pattern_book, it.get("text"))
        result.append(d[0])
    return result


if __name__ == '__main__':
    for s in cz_dic.keys():
        versions = get_version(xd='2', channel=s)
        for item in versions:  # ['语文', '2', '北师大版', '10426']
            books = get_book(item[-1])
            for book in books:  # '1436','七年级上册（2016）'
                item.append(book[1])
                item.append(book[0])
                units = get_book(book[0])
                if units:
                    for unit in units:  # ('22783', '第一单元 成长的足迹')
                        chapters = get_book(unit[0])
                        if chapters:
                            print(chapters)
