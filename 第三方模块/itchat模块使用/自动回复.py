import itchat
from itchat.content import *
@itchat.msg_register(INCOME_MSG)
def simple_reply(msg):
    print("消息类型",msg['Type'])
    print("消息内容:",msg['Content'])
    # print("消息id-->",msg['MsgId'])
    # print("消息时间-->",msg['CreateTime'])
    # print("消息发送人昵称-->",(itchat.search_friends(userName=msg['FromUserName']))["NickName"])
    # if msg['Type'] == TEXT:
    #     print("消息类型-->",'文本')
    #     print("消息内容-->",msg['Content'])
    # elif msg['Type'] == PICTURE:
    #     print("消息类型-->",'图片')
    #     print("文件名称-->",msg['FileName'])
    # elif msg['Type'] == SHARING:
    #     print("消息类型-->",'分享')
    #     print("分享的链接-->",msg['Url'])
    print("-----------------------------")
    # itchat.send_msg('nice to meet you',msg['FromUserName'])
itchat.auto_login(hotReload=True)
itchat.run()