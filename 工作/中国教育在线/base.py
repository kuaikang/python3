import requests
from bs4 import BeautifulSoup


# 更多专业
def major_more(number):
    url = "http://gkcx.eol.cn/schoolhtm/specialty/specialtyList/specialty%s.htm" % number
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content.decode(), "lxml")
    lis = soup.find(attrs={"class": "li-major grid"}).select("li")
    return [li.text for li in lis]


# 重点专业
def major_important(soup):
    majors = soup.find(attrs={"class": "li-text-label grid"}).select("li")
    data = []
    for m in majors:
        a = m.find("a")
        data.append([a["title"], a["href"]])
    return data


# 基本信息
def base_info(soup):
    info1 = soup.find(attrs={"class": "li-collegeInfo"}).select("span")
    info2 = soup.find(attrs={"class": "li-collegeInfo li-ellipsis"}).select("span")
    data = []
    for info in info1:
        data.append(info.text)
    for info in info2:
        data.append(info.text)
    return data


# 学校简介
def simple_info(soup):
    url = "http://gkcx.eol.cn/"
    for menu in soup.find(attrs={"class": "s_nav menu_school"}).select("li"):
        if menu.text == '学校简介':
            url += menu.find("a")["href"]
    response = requests.get(url)
    soup1 = BeautifulSoup(response.content.decode(), "lxml")
    response.close()
    return soup1.find(attrs={"class": "content news"})


# 招生专业
def enrol_students(number):
    url = "http://gkcx.eol.cn/schoolhtm/specialty/specialtyList/specialty%s.htm" % number
    response = requests.get(url)
    soup = BeautifulSoup(response.content.decode(),"lxml")
    response.close()
    return [x.text for x in soup.find(attrs={"class":"li-major grid"}).select("a")]


# 收费标准
def money_standard(soup):
    url = "http://gkcx.eol.cn/"
    url_money = ""
    for menu in soup.find(attrs={"class": "li-aboutCollege"}).select("li"):
        if menu.text == '收费标准':
            url_money = url + menu.find("a")["href"]
    response = requests.get(url_money)
    soup1 = BeautifulSoup(response.content.decode(), "lxml")
    return soup1.find(attrs={"class": "content news"}).select("p")[-1]


# 学校风光
def school_view(soup):
    url = "http://gkcx.eol.cn"
    url_view = ""
    for menu in soup.find(attrs={"class": "s_nav menu_school"}).select("li"):
        if menu.text == '校园风光':
            url_view = url + menu.find("a")["href"]
    response = requests.get(url_view)
    beautiful_soup = BeautifulSoup(response.content.decode(), "lxml")
    src = []
    for image in beautiful_soup.find(attrs={"id": "container"}).find_all(attrs={"class": "images"}):
        src.append(url + image.select("img")[0]["src"])
    return src


if __name__ == '__main__':
    number = "30"
    response = requests.get("http://gkcx.eol.cn/schoolhtm/schoolTemple/school%s.htm" % number)
    soup = BeautifulSoup(response.content.decode(), "lxml")
    response.close()
    print("学校简介")
    print(simple_info(soup))
    print("收费标准")
    print(money_standard(soup))
    print("基本信息")
    print(base_info(soup))
    print("重点专业")
    print(major_important(soup))
    print("更多专业")
    print(major_more(number))
    print("学校风光")
    print(school_view(soup))
    print("招生专业")
    print(enrol_students(number))
