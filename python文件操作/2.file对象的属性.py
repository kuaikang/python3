f = open("test.txt","r")
print("文件名",f.name)
print("文件打开时使用的模式",f.mode)
print("文件是否可写:",f.writable())
print("文件是否可读:",f.readable())
f.close()
if f.closed: # 文件对象是否已关闭
    print("文件已关闭")