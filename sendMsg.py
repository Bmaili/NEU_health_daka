#邮件发送依赖
from email.mime.text import MIMEText
from email.header import Header
import smtplib
#Server酱发送依赖
import requests
#环境变量
import config

class sendEmail():

    def __init__(self):
        self.sender = config.sender
        self.receiver = config.receiver
        self.mailHost = config.mailHost
        self.mailUser = config.sender
        self.mailPass = config.mailPass
    
    def sendCheck(self):
        return self.sender=='' or self.receiver=='' or self.mailHost=='' or self.mailUser=='' or self.mailPass==''

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



class sendServerChan():
  def __init__(self):
      self.sckey=config.sckey

  def sendMessage(self, message):
      url = 'https://sctapi.ftqq.com/' + self.sckey + '.send'
      data = {
          'title': '健康打卡通知',
          'desp': message
      }
      requests.post(url, data)


class sendMsg():
    def __init__(self):
        self.sckey=config.sckey
        self.mailReciver=config.receiver
        self._sendEmail=sendEmail()
        self._sendServerChan=sendServerChan()


    def sendMessage(self, message):
            if(self.sckey!=''):
                self._sendServerChan.sendMessage(message)
            if(self.mailReciver!=''):
                self._sendEmail.sendMessage(message)

if __name__ == '__main__':
    _sendMsg=sendMsg()
    _sendMsg.sendMessage('测试')