score = int(input("please input your score:"))
if score >= 90 and score <= 100:
    print(score,"--> 优秀")
elif score >= 80 and score < 90:
    print(score,"--> 良好")
elif score >= 70 and score < 80:
    print(score,"--> 中等")
elif score >= 60 and score < 70:
    print(score,"--> 及格")
else:
    print("不及格")


