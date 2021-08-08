import re
import time
import requests
import sendEmail
import config


class daka():
    def __init__(self):
        self.id = config.stutendID
        self.password = config.passward
        self.token = ""
        self.name = ""
        self.lt = ""
        self.my_session = requests.session()
        self.sendEmail = sendEmail.sendEmail()

        self.login_url = 'https://e-report.neu.edu.cn/login'
        self.create_url = 'https://e-report.neu.edu.cn/notes/create'
        self.note_url = 'https://e-report.neu.edu.cn/api/notes'


    def login(self):
        #登陆，更新session
        try:
            login_response = self.my_session.get(self.login_url)
            self.lt = re.findall(r'LT-[0-9]*-[0-9a-zA-Z]*-tpass', login_response.text, re.S)[0]
            post_url = 'https://pass.neu.edu.cn' + re.findall(r'\/tpass\/login[^\"] *', login_response.text, re.S)[0]

            login_form_items = {
                'rsa': self.id + self.password + self.lt,
                'ul': str(len(self.id)),
                'pl': str(len(self.password)),
                'lt': self.lt,
                'execution': 'e1s1',
                '_eventId': 'submit'
            }
            post_response = self.my_session.post(post_url, login_form_items)
        except:
            if config.isSendMessage:
                self.sendEmail.sendMessage('健康打卡登录失败！请手动完成打卡！')


    def healthDaka(self):
        #健康打卡
        try:
            note_response = self.my_session.get(self.create_url)
            self.token = re.findall(r'name=\"_token\"\s+value=\"([0-9a-zA-Z]+)\"',note_response.text, re.S)[0]
            self.name = re.findall(r'当前用户：\s*(\w+)\s*', note_response.text, re.S)[0]

            health_items = {
                '_token': self.token,
                'jibenxinxi_shifoubenrenshangbao': '1',
                'profile[xuegonghao]': self.id,
                'profile[xingming]': self.name,
                'profile[suoshubanji]': '',
                'jiankangxinxi_muqianshentizhuangkuang': '正常',
                'xingchengxinxi_weizhishifouyoubianhua': '0',
                'cross_city': '无',
                'qitashixiang_qitaxuyaoshuomingdeshixiang': ''
            }
            health_response = self.my_session.post(self.note_url, health_items)
            if health_response.status_code == 201:
                print(str(health_response) + '健康打卡成功')
            elif config.isSendMessage:
                self.sendEmail.sendMessage('健康打卡失败！请手动完成打卡！' + str(health_response))
        except:
            if config.isSendMessage:
                self.sendEmail.sendMessage('健康打卡失败！请手动完成打卡！')


    def temperatureDaka(self):
        #体温打卡
        try:
            hour = (time.localtime().tm_hour + 8) % 24   # 加8是因为腾讯云跑出来是格林时间
            temperature_url = 'https://e-report.neu.edu.cn/inspection/items/{}/records'.format(('1' if 7 <= hour <= 9 else '2' if 12 <= hour <= 14 else '3'))
            temperature_items = {
                '_token': self.token,
                'temperature': '36.5',
                'suspicious_respiratory_symptoms': '0',
                'symptom_descriptions': ''
            }
            temperature_response = self.my_session.post(temperature_url,    temperature_items)
            if temperature_response.status_code == 200:
                    print(str(temperature_response) + '体温打卡成功')
            elif config.isSendMessage:
                self.sendEmail.sendMessage('体温打卡失败！请手动完成打卡！' + str(temperature_response))
        except:
            if config.isSendMessage:
                self.sendEmail.sendMessage('体温打卡失败！请手动完成打卡！')

def main_handler(event, context):
    _daka=daka()
    _daka.login()
    _daka.healthDaka()
    _daka.temperatureDaka()

if __name__ == '__main__':
    main_handler(None,None)