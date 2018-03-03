import hashlib

md5 = hashlib.md5(b"123")  # 返回一个md5对象，如果给出参数，则相当于调用了update(arg)
md5.update(b'456')
print(md5.hexdigest())  # 以16进制的形式返回摘要，32位

print(hashlib.sha1(b'123456').hexdigest())  # 40位
