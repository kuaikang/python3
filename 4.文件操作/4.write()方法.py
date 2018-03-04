import json

# f = open("test_write.txt","w",encoding="utf-8")
# f.write("HelloWorld\n")
# f.write("HelloWorld\n")
# f.close()

f = open("test_write.txt", "w", encoding="utf-8")
lines = ["1", "2", "3", "4", "5"]
# lines = [line+'\n' for line in lines]
f.writelines(lines)  # 写入一个列表
f.close()

# json 写入到文件
dict = {"key1": "val2", "key2": "val2", "key3": "val3"}
with open("test.txt", mode="a", encoding="utf8") as f:
    for i in range(10):
        f.write(json.dumps(dict, ensure_ascii=False))
        f.write("\n")
