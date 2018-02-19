from urllib import request,error
try:
    response = request.urlopen("http://bai11.com")
except error.HTTPError as r:
    print(type(r.reason))
    print(r.reason,r.code,r.headers)
except error.URLError as e:
    print(e.reason)


'''
URLError只有reason属性,HTTPError有code、reason、headers三个属性
HTTPError是URLError的子类
'''