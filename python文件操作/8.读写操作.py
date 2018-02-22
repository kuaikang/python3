with open("test.txt","rb") as f1,open("test_new.txt","wb") as f2:
    for line in f1:
        f2.write(line)

# 边读编写,实现文件的复制