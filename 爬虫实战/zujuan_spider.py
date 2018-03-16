url = "http://www.zujuan.com"
resp = requests.get(url)
soup = BeautifulSoup(resp.text, "lxml")
f = open("cookie_zujuan", mode="r", encoding="utf8")
cookie = f.readline().strip()
f.close()
head = {
    "Cookie": cookie
}

