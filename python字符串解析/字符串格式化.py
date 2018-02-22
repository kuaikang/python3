msg1 = "my name is {} , and age is {}"
msg2 = "my name is {0} , and age is {1}"
msg3 = "my name is {name} , and age is {age}"
print(msg1.format("tom",24))
print(msg2.format("jack",24))
print(msg3.format(name="lucy",age=22))
print(msg3.format_map({"name":"lily","age":"19"}))