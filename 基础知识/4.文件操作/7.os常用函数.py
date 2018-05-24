import os
print(os.getcwd()) # 当前工作目录
# os.chdir("E:\\python3.6") # 改变工作目录
print(os.getcwd())

# os.rmdir("E:\\a") # 删除空文件夹

print("路径分隔符",os.sep)
print("操作系统",os.name) # 操作系统的名称,对于Windows返回'nt',而对于Linux/Unix用户，它是'posix'
print("环境变量-->path",os.getenv("path")) # path

print(os.listdir("E:\\python3.6")) # 返回指定目录下的所有文件和目录名(一级目录和文件)
# os.remove("E:\\a.txt") 删除指定文件
# print(os.system("dir")) # 用来运行shell命令,windows是cmd命令
print(os.linesep)# 字符串给出当前平台使用的行终止符。例如，Windows使用'\r\n'，Linux使用'\n'而Mac使用'\r'。
print("当前目录",os.curdir)


# os.path.isfile()和os.path.isdir()函数分别检验给出的路径是一个文件还是目录。
# os.path.existe()函数用来检验给出的路径是否真地存在
# os.path.getsize(name):获得文件大小，如果name是目录返回0L
# os.path.abspath(name):获得绝对路径
# os.path.normpath(path):规范path字符串形式
# os.path.split(path) ：将path分割成目录和文件名二元组返回。
# os.path.splitext():分离文件名与扩展名
# os.path.join(path,name):连接目录与文件名或目录
# # os.path.basename(path):返回文件名
# # os.path.dirname(path):返回文件路径