import requests
# data = {"name":"tony","age":"23"}
# headers = {
#      "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                   "Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
# }
# files = {"file":open("icon.jpg",mode="rb")}
# response = requests.post("http://httpbin.org/post",data=data,files=files)
# exit() if not response.status_code == 200 else print("request successfully")
# print(type(response.status_code),response.status_code)
# print(type(response.headers),response.headers)
# print(type(response.cookies),response.cookies)
# print(type(response.url),response.url)
# print(type(response.history),response.history)
# print(response.text)

# 获取cookie
# response = requests.post("http://www.baidu.com")
# print(type(response.cookies))
# for key,value in response.cookies.items():
#     print(key+"="+value)

# 会话维持
# ses = requests.Session()
# ses.get("http://httpbin.org/cookies/set/number/123456789")
# response = ses.get("http://httpbin.org/cookies")
# print(response.text)

# https协议需要先进行证书验证
# import urllib3
# urllib3.disable_warnings() # 不打印警告信息
# response = requests.get("https://www.12306.cn",verify=False)
# print(response.status_code)

# 代理设置
# proxies = {
#     "http":"http://127.0.0.1:9573",
#     "https":"https://user:password@127.0.0.1:9572" # 用户名密码
# }
# response = requests.get("http://www.taobao.com",proxies=proxies)
# print(response.status_code)

# 超时设置
# requests.get("http://www.baidu.com",timeout=1)

# 访问页面就需要登录,例如rabbitmq
# from requests.auth import HTTPBasicAuth
# # response = requests.get("http://120.27.34.21:9001",auth=HTTPBasicAuth("user","password"))
# response = requests.get("http://120.27.34.21:9001",auth=("user","password"))
# print(response.status_code)

# 异常处理

