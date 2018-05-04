import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    resp = requests.get(url='https://www.cnblogs.com/wang-meng/p/5701990.html')
    soup = BeautifulSoup(resp.text, 'lxml')
    print(soup.find(attrs={"id": "cnblogs_post_body"}).text)
