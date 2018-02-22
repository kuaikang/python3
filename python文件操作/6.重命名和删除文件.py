import shutil,os
# 复制并重命名单个文件 old_file new_file
# shutil.copy("E:\\a.txt","E:\\b.txt")

# 复制整个目录(备份)
# shutil.copytree("E:\\a","E:\\new_a")

# 删除文件
# os.unlink("E:\\b.txt")

# 删除空文件夹
try:
    os.rmdir("E:\\b")
except Exception as ex:
    print("错误信息："+str(ex))#提示：错误信息，目录不是空的

# 删除文件夹及内容
# shutil.rmtree("E:\\b")

#重命名文件
# shutil.move("E:\\a.txt","E:\\a_new.txt")

#重命名文件夹
# shutil.move("E:\\a","E:\\new_a")
