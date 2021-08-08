from email.mime.text import MIMEText
from email.header import Header
import smtplib
import config

class sendEmail():

    def __init__(self):
        self.sender = config.sender
        self.receiver = config.receiver
        self.mailHost = 'smtp.qq.com'
        self.mailUser = config.sender
        self.mailPass = config.mailPass

    def sendMessage(self , message):
        # 邮件普通文本内容
        mailContent = message
        message = MIMEText(mailContent, 'plain', 'utf-8')
        # 发送人名称
        message['From'] = Header('健康打卡通知', 'utf-8')
        # 收件人名称
        message['To'] = Header(self.receiver, 'utf-8')
        # 邮件标题
        message['Subject'] = Header('健康打卡通知', 'utf-8')

        try:
            smtpObj = smtplib.SMTP_SSL(self.mailHost, 465)
            smtpObj.login(self.mailUser, self.mailPass)
            smtpObj.sendmail(self.sender, self.receiver, message.as_string())
        except smtplib.SMTPException:
            print('Error: 无法发送邮件')


if __name__ == '__main__' :
    _sendEmail = sendEmail()
    _sendEmail.sendMessage('这是一条测试信息')
