from selenium import webdriver

from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('Cookie')
driver = webdriver.Chrome(chrome_options=chrome_options)


def write_unit(browser, categories, bookversion, nianji, chid, xd):
    url = "http://www.zujuan.com/question?categories=%s&bookversion=%s&nianji=%s&chid=%s&xd=%s"
    browser.get(url % (categories, bookversion, nianji, chid, xd))
    f = open("a.txt", "w", encoding="utf8")
    f.write(browser.page_source)
    f.close()


def insert_unit(file_name, bookversion):
    f = open("a.txt", mode="r", encoding="utf8")
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, "lxml")
    tree = soup.find_all(attrs={"id": "J_Tree"})
    ts = tree[0].find_all("a")
    ids = html[html.find("fetchTree"):html.find("function fetchTree")]
    ids = ids[ids.find("[{") + 1:ids.find("]")]
    ids = ids.split(":")
    f = open(file_name, mode="a", encoding="utf8")
    for i in range(1, len(ids), 3):
        f.write(bookversion + "," + ts[(i - 1) // 3].get_text().strip() + "," + ids[i].split(",")[0][1:-1])
        f.write("\n")
    f.close()
