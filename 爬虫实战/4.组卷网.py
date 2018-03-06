import requests
from bs4 import BeautifulSoup

url = "http://www.zujuan.com"
resp = requests.get(url)
soup = BeautifulSoup(resp.text, "lxml")


def get_xx():
    data = soup.find(attrs={"class": "list-xx"}).select('a')
    return data


def get_cz():
    return soup.find(attrs={"class": "list-cz"}).select('a')
    return data


def get_gz():
    return soup.find(attrs={"class": "list-gz"}).select('a')


def parse_data_subject(data, str):
    for index in data:
        yield {
            "href": url + index.attrs['href'],
            "subject": str + index.get_text()
        }
    return data


def get_units(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")
    data = soup.find(attrs={"id": "J_Tree"}).select('a')
    return [x.get_text() for x in data]


def teaching_material(url):  # 教材
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")
    data = soup.find_all(attrs={"class": "con-items"})[0].select('a')
    for index in data:
        yield {
            "href": url + index.attrs['href'],
            "meterial": index.get_text()
        }
    return data
    # data[0]教材  data[1]年级  data[2]题型  data[3]难易程度  data[4]题类筛选  data[5]知识点个数  data[6]


def grades(url):  # 年级
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")
    data = soup.find_all(attrs={"class": "con-items"})[1].select('a')
    for index in data:
        yield {
            "href": url + index.attrs['href'],
            "grade_name": index.get_text()
        }
    return data


if __name__ == '__main__':
    xx = parse_data_subject(get_xx(), "小学")
    cz = parse_data_subject(get_cz(), "初中")
    gz = parse_data_subject(get_gz(), "高中")
    f = open("a.txt", mode="a", encoding="utf8")
    for index in xx:  # index["href"], index["subject"]
        data = teaching_material(index["href"][:-8]) # index['meterial']
        for i in data:
            data = grades(i["href"])  # j["grade_name"]]
            for j in data:
                li = [index["subject"], i["meterial"], j["grade_name"]]
                f.write(",".join(li))
                f.write("\n")
                # units = get_units(j["href"])
                # print(units)
    f.close()