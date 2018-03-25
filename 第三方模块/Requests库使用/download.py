import requests

if __name__ == '__main__':

    resp = requests.get(url="url", stream=True)
    f = open("http://www.baidu.com", mode="wb")
    for chunk in resp.iter_content(chunk_size=2048):
        if chunk:
            f.write(chunk)
    f.close()
