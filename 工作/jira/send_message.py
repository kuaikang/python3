import smtplib
from email.mime.text import MIMEText

msg_from = '359405466@qq.com'  # 发送方邮箱
password = 'owonffeaotpkbijh'  # 填入发送方邮箱的授权码


def send_message(title, content, msg_to):
    try:
        msg = MIMEText(content)
        msg['Subject'] = title
        msg['From'] = msg_from
        msg['To'] = msg_to
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
        s.login(msg_from, password)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print("发送成功")
    except s.SMTPException:
        print("发送失败")
    finally:
        s.quit()


if __name__ == '__main__':
    send_message("主题", "you have new bug", "359405466@qq.com")
