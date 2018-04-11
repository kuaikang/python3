import requests
from bs4 import BeautifulSoup
import json
import re

res_type = {"2": "图片素材", "3": "电子教案", "16": "教学课件", "14": "音频", "15": "视频"}
headers = {
    "Cookie": "JSESSIONID=3797F1B8B08BEBED55489CC3AA69757C"
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
            grades_url.append([a.text, base_url + a['href']])
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
        max_page = soup.find(attrs={"class": "pager"}).select('span')[-1].text
        data = []
        for item in soup.find_all(attrs={"style": "cursor:pointer;"}):
            if item.text:
                res_id = item['onclick'].split(',')[-1][:-2]
                data.append([res_id, item.text])
        return data, max_page


def write_file():
    f = open("doc/resource,.txt", mode="a", encoding="utf8")
    for res in res_type:
        grade_arr = get_grade_url(res)
        for grade in grade_arr:  # 年级
            books = get_book_url(grade[1])
            for book in books:  # 课本
                units = get_unit_url(book[1])
                for unit in units:  # 单元
                    # 类型,年级,课本,单元,地址
                    data = {"type": res, "grade": grade[0], "book": book[0], "unit": unit[0], "url": unit[1]}
                    print(data)
                    f.write(json.dumps(data, ensure_ascii=False))
                    f.write("\n")
    f.close()


pattern = re.compile('.*?filename="(.*?)"', re.S)


def download(line, url):
    with requests.get(url=url,headers=headers, stream=True) as resp:
        file_name = re.findall(pattern, resp.headers.get('Content-disposition'))[-1]
        f = open(file_name, mode="wb")
        for chunk in resp.iter_content(chunk_size=2048):
            if chunk:
                f.write(chunk)
        f.close()


def main():
    with open("doc/resource,.txt", mode="r", encoding="utf8") as f:
        for line in f.readlines():
            line = json.loads(line.strip())
            if line.get('type') in ['2', '14', '15']: continue
            for i in range(1, 100):
                data, page = get_resource(url=line.get("url"), page_num=i)
                for item in data:
                    url = "http://www.slbyy.com/outline/download?outlineId=1328"
                    download(line,)
                    print(item, page)

                if not data or page == i: break


if __name__ == '__main__':
    main()

    # resp = requests.get('http://www.slbyy.com/outline/download?outlineId=1589', headers=headers)
    # print(re.findall(pattern, resp.headers.get('Content-disposition'))[-1])
