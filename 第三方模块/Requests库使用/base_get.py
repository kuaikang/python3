import requests,json
# data = {
#     "name":"tony",
#     "age":"22"
# }
# response = requests.get("http://httpbin.org/get",params=data)
# print(response.text)

# # 解析json,如果返回数据是json
# response = requests.get("http://httpbin.org/get")
# print(response.json())

response = requests.get("https://github.com/favicon.ico")
print("response.text返回类型:",type(response.text))
# print("response.content返回类型:",type(response.content))

# headers = {
#     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                  "Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
# }
# response = requests.get("http://www.zhihu.com/explore",headers=headers)
# print(response.text)