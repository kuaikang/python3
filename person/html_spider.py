import requests
from common.request_util import headers
from bs4 import BeautifulSoup


def get_urls():
    resp = requests.get("https://zhuanlan.zhihu.com/p/33935046", headers=headers)
    soup = BeautifulSoup(resp.text, 'lxml')
    for item in soup.find_all(attrs={"class": "internal"}):
        print(item)


def parse_url():
    resp = requests.get("https://zhuanlan.zhihu.com/p/33674237", headers=headers)
    soup = BeautifulSoup(resp.text, 'lxml')
    print(soup.find(attrs={"class": "RichText ztext Post-RichText"}))


if __name__ == '__main__':
    parse_url()
