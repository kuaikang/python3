import requests
resp = requests.get("http://www.baidu.com")
with open("baidu.html",mode="wb") as f:
    f.write(resp.content)
print(resp.content.decode())