import requests
from common.request_util import headers

if __name__ == '__main__':
    while True:
        user_input = input(">>:")
        if user_input == 'quit()':
            break
        url = 'http://fanyi.youdao.com/openapi.do?key=79379998&keyfrom=justdoit&type=data&doctype=json&version=1.1&q=' + user_input
        print(requests.get(url, headers=headers).json().get('translation')[0])
