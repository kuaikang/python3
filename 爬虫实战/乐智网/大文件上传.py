import requests

if __name__ == '__main__':
    with open('E:\\resource\\历史\\八年级\\北师大版\\下册\\第1课 中华人民共和国成立\\第1课 中华人民共和国成立 课件1.ppt',
              mode="rb") as f:
        files = {'file': ['1.ppt', f, 'application/octet-stream']}
        resp = requests.post(url='url', files=files)
        print(resp.json())
