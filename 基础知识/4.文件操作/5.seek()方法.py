with open("test.txt",mode="r",encoding="utf-8") as f:
    print(f.readline().strip())
    f.readline()
    print("当前文件指针所在位置",f.tell())  # 获取当前文件读取指针的位置  18
    f.seek(0,0) # 重新设置文件指针到开头
    print(f.readline())

# fileObject.seek(offset[, whence])
# offset -- 开始的偏移量，也就是代表需要移动偏移的字节数
# whence：可选，默认值为 0。给offset参数一个定义，表示要从哪个位置开始偏移；0代表从文件开头开始算起，
# 1代表从当前位置开始算起，2代表从文件末尾算起。