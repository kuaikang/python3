# import urllib.request
# # def urlopen(url, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
# #             *, cafile=None, capath=None, cadefault=False, context=None):
# response = urllib.request.urlopen("https://www.baidu.com")
# print(response.read().decode("utf-8"))

# import urllib.parse,urllib.request,socket
# data = bytes(urllib.parse.urlencode({"word":"hello"}),encoding="utf-8")
# try:
#     response = urllib.request.urlopen("http://httpbin.org/post",data=data,timeout=1)
#     print(response.read().decode())
# except socket.timeout as e:
#     print("Time out")

'''状态码,响应头'''
import urllib.request
response = urllib.request.urlopen("https://python.org")
print(response.status)
# print(response.getheaders()) # 打印所有的头信息
print(response.getheader("Server"))