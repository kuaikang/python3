import requests
from urllib.parse import urlencode

if __name__ == '__main__':
    data = {

    }
    resp = requests.get("http://www.jiaoxueyun.cn/resources-more-inter!getTrees.do?")
    print(resp.text)