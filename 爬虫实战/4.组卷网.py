import requests, threading, time, json
from bs4 import BeautifulSoup
from urllib.parse import urlencode

url = "http://www.zujuan.com"
resp = requests.get(url)
soup = BeautifulSoup(resp.text, "lxml")
f = open("cookie_zujuan", mode="r", encoding="utf8")
cookie = f.readline().strip()
f.close()
head = {
    "Cookie": cookie
}


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
    resp = requests.get(url, headers=head)
    soup = BeautifulSoup(resp.text, "lxml")
    # data = soup.find(attrs={"id": "J_Tree"}).select('a')
    # ids = soup.find(attrs={"id": "J_Tree"})
    # return [x.get_text() for x in data], ids
    return resp.text


def get_chapters(id):
    req = {
        "id": id,
        "type": "category"
    }
    url = "http://www.zujuan.com/question/tree?"+urlencode(req)
    res = requests.get(url=url, headers=head)
    res = json.loads(res.text)
    return [i.get("title") for i in res]


def teaching_material(url):  # 教材
    resp = requests.get(url, headers=head)
    soup = BeautifulSoup(resp.text, "lxml")
    data = soup.find_all(attrs={"class": "con-items"})[0].select('a')
    for index in data:
        yield {
            "href": url + index.attrs['href'],
            "material": index.get_text()
        }
    return data
    # data[0]教材  data[1]年级  data[2]题型  data[3]难易程度  data[4]题类筛选  data[5]知识点个数  data[6]


def grades(url):  # 年级
    resp = requests.get(url, headers=head)
    soup = BeautifulSoup(resp.text, "lxml")
    data = soup.find_all(attrs={"class": "con-items"})[1].select('a')
    for index in data:
        yield {
            "href": "http://www.zujuan.com" + index.attrs['href'],
            "grade_name": index.get_text()
        }
    return data


def run(subject, file_name, xd):
    f = open(file_name, mode="a", encoding="utf8")
    url = "http://www.zujuan.com/question/index?"
    for key in subject.keys():
        data_dic = {"chid": subject[key], "xd": xd}
        data = teaching_material(url + urlencode(data_dic))
        for item in data:  # 教材 href material
            res = grades(item["href"])
            for j in res:
                ids = get_units(j["href"])
                print(ids)
                # re, ids = get_units(j["href"])
                # print(re)
                # print(ids)
                # for i in range(len(re)):
                #     chapters = get_chapters(ids[i])
                #     for c in chapters:
                #         li = [key, item.get("material"), j.get("grade_name"), re[i].strip(), c]
                #         f.write(",".join(li))
                #         f.write("\n")
    f.close()


if __name__ == '__main__':
    xx = {"语文": "2", "数学": "3", "英语": "3", "科学": "5", "政治思品": "9"}
    cz = {"语文": "2", "数学": "3", "英语": "4", "科学": "5", "物理": "6", "化学": "7", "历史": "8", "政治思品": "9",
          "历史与社会": "20", "生物": "11"}
    gz = {"语文": "2", "数学": "3", "英语": "3", "物理": "6", "化学": "7", "历史": "8", "政治思品": "9", "地理": "10", "生物": "11"}

    # t1 = threading.Thread(target=run, args=(xx, "小学.txt", 1))
    # t1.start()
    # t2 = threading.Thread(target=run, args=(cz, "初中.txt", 2))
    # t2.start()
    # t3 = threading.Thread(target=run, args=(gz, "高中.txt", 3))
    # t3.start()


    # 初中 "社会思品": "21", "地理": "10"