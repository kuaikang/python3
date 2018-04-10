import requests
from bs4 import BeautifulSoup

res_type = {"2": "图片素材", "3": "电子教案", "16": "教学课件"}
grade = {"三年级": "4", "四年级": "5", "五年级": "110", "六年级": "112"}
headers = {
    "Cookie": "JSESSIONID=AA2E3044E11ECA2A288E1972B172D310"
}

base_url = "http://www.slbyy.com"


def get_grade_url(r_type):
    url = "http://www.slbyy.com/outline?outlineClassId={res_type}".format(res_type=r_type)
    with requests.get(url, headers=headers) as resp:
        return parse_html(resp.text)


def parse_html(html):
    soup = BeautifulSoup(html, "lxml")
    grades = soup.find(attrs={"class": "screen"}).select("dl")[-1].select("span")
    grades_url = []
    for g in grades:
        a = g.find("a")
        if a.text != "全部":
            grades_url.append({a.text: base_url + a['href']})
    return grades_url


def get_book_url(url):
    with requests.get(url, headers=headers) as resp:
        return parse_html(resp.text)


def get_unit_url(url):
    with requests.get(url, headers=headers) as resp:
        return parse_html(resp.text)


def get_resource(url, page_num):
    with requests.get(url.format(pageNum=page_num), headers=headers) as resp:
        soup = BeautifulSoup(resp.text, "lxml")
        data = []
        for item in soup.find_all(attrs={"style": "cursor:pointer;"}):
            if item.text:
                res_id = item['onclick'].split(',')[-1][:-2]
                data.append({res_id: item.text})
        return data


if __name__ == '__main__':
    res = get_resource('http://www.slbyy.com/outline?outlineClassId=5', 1)
    print(res)
