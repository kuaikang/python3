from urllib import request,parse
url = "" # 请求路径
headers={ # 头信息

}
dict={} # 传参
data = bytes(parse.urlencode(dict),encoding="utf8")
req = request.Request(url=url,data=data,headers=headers,method="POST")
# req.add_header("content-type","application/json") 可以通过add_header增加头信息
response = request.urlopen(req)
