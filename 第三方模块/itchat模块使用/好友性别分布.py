import itchat

itchat.auto_login()
friends = itchat.get_friends(update=True)[:]
total = len(friends) - 1
man = women = other = 0

for friend in friends[0:]:
    sex = friend["Sex"]
    if sex == 1: # 1代表男生
        man += 1
    elif sex == 2: # 2代表女生
        women += 1
    else:
        other += 1

print("男性好友",man)
print("女性好友",women)
print("其他",other)
itchat.send("男性好友%s 女性好友%s 其他%s"%(man,women,other),'filehelper')