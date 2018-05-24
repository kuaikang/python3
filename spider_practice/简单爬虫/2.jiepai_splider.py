import requests,json
from urllib.parse import urlencode
def get_page_index():
    params = {
        'offset': '0',
        'format': 'json',
        'keyword': '街拍',
        'autoload':'true',
        'count': '20',
        'cur_tab':'1',
        'from':'search_tab'
    }
    resp = requests.get("https://www.toutiao.com/search/?"+urlencode(params))
    return resp.text

def main():
    html = get_page_index()
    print(html)
if __name__ == '__main__':
    main()