# f = open("test_write.txt","w",encoding="utf-8")
# f.write("HelloWorld\n")
# f.write("HelloWorld\n")
# f.close()

f = open("test_write.txt","w",encoding="utf-8")
lines = ["1","2","3","4","5"]
# lines = [line+'\n' for line in lines]
f.writelines(lines) # 写入一个列表
f.close()

