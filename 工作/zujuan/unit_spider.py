from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('Cookie')
driver = webdriver.Chrome(chrome_options=chrome_options)


def write_file(categories, bookversion, nianji, chid, xd, header):
    url = "http://www.zujuan.com/question?categories=%s&bookversion=%s&nianji=%s&chid=%s&xd=%s" % (
        categories, bookversion, nianji, chid, xd)
    driver.get(url, headers=header)
    f = open("a.txt", "w", encoding="utf8")
    f.write(driver.page_source)
    f.close()



f = open("a.txt", mode="r", encoding="utf8")
html = f.read()
f.close()
soup = BeautifulSoup(html, "lxml")
tree = soup.find_all(attrs={"id": "J_Tree"})
ts = tree[0].find_all("a")
ids = html[html.find("fetchTree"):html.find("function fetchTree")]
ids = ids[ids.find("[{") + 1:ids.find("]")]
ids = ids.split(":")
for i in range(1, len(ids), 3):
    print(ts[(i - 1) // 3].get_text().strip() + "," + ids[i].split(",")[0][1:-1])
