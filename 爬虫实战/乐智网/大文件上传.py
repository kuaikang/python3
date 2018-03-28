import requests

if __name__ == '__main__':
    with open('E:\\question\\1522217253.102.png',
              mode="rb") as f:
        files = {'file': ['1.png', f, 'application/octet-stream']}
        resp = requests.post(url='http://dfs.upload1.jzexueyun.com/cos/upload', files=files)
        print(resp.json())
