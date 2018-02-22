print("read()".center(50,"-"))
f = open("test.txt","r",encoding="utf-8")
print(f.read(14)) # 10表示从文件中读取的字节数.不填则表示读取所有
f.close()

print("readline()".center(50,"-"))
f = open("test.txt","r",encoding="utf-8")
print(f.readline().strip())
print(f.readline())
f.close()

print("readlines()".center(50,"-"))
f = open("test.txt","r",encoding="utf-8")
data = f.readlines() # 得到的是一个列表,每行是一个元素
print(data)
f.close()

f = open("test.txt","r",encoding="utf-8")
for line in f:
    print(line.strip())
f.close()