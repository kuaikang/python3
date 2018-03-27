import requests
from bs4 import BeautifulSoup


def get_proxy():
    resp = requests.get('http://31f.cn/')
    soup = BeautifulSoup(resp.text, 'lxml')
    trs = soup.find(attrs={'class': 'table table-striped'}).select('tr')
    for tr in trs[1:]:
        tds = tr.select('td')
        index = tds[0].text
        ip = tds[1].text
        port = tds[2].text
        protocol = tds[4].select_one('a').text
        print(index, ip, port, protocol)


if __name__ == '__main__':
    proxies = {
        'http': 'http://140.143.134.248:3128',
        'https': 'https://140.143.134.248:3128'
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/65.0.3325.146 Safari/537.36'
    }
    resp = requests.get("http://www.baidu.com", proxies=proxies)
    print(resp.headers)
