import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    response = requests.get("http://www.eol.cn/html/g/fsx/index.shtml")
    html = response.text.encode("iso-8859-1").decode('gbk')
    response.close()
    soup = BeautifulSoup(html, "lxml")
    completes = soup.find(attrs={"class": "area-con clearfix"})
    for item in completes.find_all(attrs={"class": "area-item"}):
        print(item.find(attrs={"class": "area-name"}).text)  # 省份
        for year in item.find_all(attrs={"class": "area-tab-item"}):
            print(year.text, end=",")
        print()
        tables = item.select("table")
        for table in tables:
            trs = table.select("tr")
            for tr in trs:
                tds = tr.select("td")
                for td in tds:
                    print(td.text, end=",")
                print()
            print()
