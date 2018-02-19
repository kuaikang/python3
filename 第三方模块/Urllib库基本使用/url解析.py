from urllib.parse import urlparse
# result = urlparse("http://www.baidu.com/index.html;user?id=5#comment")
# print(type(result),result)

# scheme 协议类型
result = urlparse("www.baidu.com/index.html;user?id=5#comment",scheme="https")
print(type(result),result)

# 假如没有协议内容就以scheme为准
# result = urlparse("http://www.baidu.com/index.html;user?id=5#comment",scheme="https")
# print(type(result),result)

# result = urlparse("http://www.baidu.com/index.html;user?id=5#comment",allow_fragments=False)
# print(type(result),result)

from urllib.parse import urlunparse
data = ["http","www.baidu.com","index.html","user","id=5","comment"]
print(urlunparse(data))

from urllib.parse import urljoin
print(urljoin("http://www.baidu.com","index.html"))
print(urljoin("http://www.baidu.com","http://www.python.org"))

from urllib.parse import urlencode
params = {
    "name":"tom",
    "addr":"china"
}
base_url = "http://www.baidu.com?"
url = base_url + urlencode(params)
print(url) # urlencode把字典变成get请求参数