print("字典是key-value的数据类型".center(50, "-"))
print("字典是无序的，key不能重复")
info = {"stu1": "tom", "stu2": "jack", "stu3": "lucy"}
print(info)
# 添加
info["stu4"] = "bob"
# 修改
info["stu1"] = "zhang"
# 删除
# info.pop("stu2") # 标准删除方法
# del info["stu3"]
# 查找
print('-----',info.get("stu11"))  # 不存在的时候返回
# print(info["stu0"]) # 不存在时会报错
print(info)

print()
import sys

for key in info.keys():
    sys.stdout.write(key + " ")
print()
for val in info.values():
    sys.stdout.write(val + " ")
print()
for key, val in info.items():
    sys.stdout.write(key + "-->" + val + "  ")
