import requests

if __name__ == '__main__':
    with open('E:\\resource\\ls\\八年级\\北师大版\\下册\\第三单元 建设中国特色社会主义\\第10课 伟大的历史转折 课件1.ppt',
              mode="rb") as f:
        files = {'file': ['1.ppt', f, 'application/octet-stream']}
        resp = requests.post(url='http://dfs.upload1.jzexueyun.com/cos/upload', files=files)
        print(resp.json())
