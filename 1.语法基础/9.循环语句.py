import sys, time

# 用for循环实现进度条
for i in range(10):
    sys.stdout.write("*")
    sys.stdout.flush()
    time.sleep(0.1)
else:  # 只有当循环正常结束(执行完毕)时才执行else
    print("循环正常结束...")

count = 0
sum = 0
while count <= 100:
    sum += count
    count += 1
else:
    print("\n", sum)  # 100以内整数相加的结果
# while循环注意不要进入死循环了
