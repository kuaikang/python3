import itchat
import math
import os
import PIL.Image as Image

#给auto_login方法传入值为真的hotReload.即使程序关闭，一定时间内重新开启也可以不用重新扫码
itchat.auto_login()
friends = itchat.get_friends(update=True)

#下载所有好友的头像图片
num = 0
for i in friends:
 img = itchat.get_head_img(i["UserName"])
 with open('headImg/' + str(num) + ".jpg",'wb') as f:
  f.write(img)
  f.close()
  num += 1
#获取文件夹内的文件个数
length = len(os.listdir('headImg'))
#根据总面积求每一个的大小
each_size = int(math.sqrt(float(810*810)/length))
#每一行可以放多少个
lines = int(810/each_size)
#生成白色背景新图片
image = Image.new('RGB', (810, 810),'white')
x = 0
y = 0
for i in range(0,length):
 try:
  img = Image.open('./headImg/' + str(i) + ".jpg")
 except IOError:
  print(i)
  print("Error")
 else:
  img = img.resize((each_size, each_size), Image.ANTIALIAS) #resize image with high-quality
  image.paste(img, (x * each_size, y * each_size))
  x += 1
  if x == lines:
   x = 0
   y += 1
image.save('headImg/' + "all.jpg")
#通过文件传输助手发送到自己微信中
itchat.send_image('headImg/' + "all.jpg",'filehelper')
image.show()