# break跳出循环,continue跳过此次循环,继续下一次
for i in range(100):
    if i > 50:
        print(i)
        break

for i in range(10):
    if i % 2 == 0:
        continue  # 偶数时跳过
    print(i)
