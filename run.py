import re
import time
import requests
import sendMsg
import config


class daka():
    def __init__(self):
        self.id = config.stutendID
        self.password = config.passward
        self.token = ""
        self.name = ""
        self.lt = ""
        self.my_session = requests.session()
        self.sendMsg=sendMsg.sendMsg()

        self.login_url = 'https://e-report.neu.edu.cn/login'
        self.post_url = 'https://pass.neu.edu.cn/tpass/login'
        self.create_url = 'https://e-report.neu.edu.cn/notes/create'
        self.note_url = 'https://e-report.neu.edu.cn/api/notes'


    def login(self):
        #登陆，更新session
        msg=''
        try:
            login_response = self.my_session.get(self.login_url)
            self.lt = re.findall(r'LT-[0-9]*-[0-9a-zA-Z]*-tpass', login_response.text, re.S)[0]
            
            login_form_items = {
                'rsa': self.id + self.password + self.lt,
                'ul': str(len(self.id)),
                'pl': str(len(self.password)),
                'lt': self.lt,
                'execution': 'e1s1',
                '_eventId': 'submit'
            }
            post_response = self.my_session.post(self.post_url, login_form_items)
            msg=config.stutendID+'登录成功!'
        except:
            msg=config.stutendID+'登录失败!请手动完成打卡!'
        return msg


    def healthDaka(self):
        #健康打卡
        msg=''
        success=False
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
                msg=config.stutendID+'健康打卡成功!'
                success=True
            else:
                msg=config.stutendID+'健康打卡失败！请手动完成打卡！'+ '(响应异常)'+str(health_response)
        except:
                msg=config.stutendID+'健康打卡失败！请手动完成打卡！'+ '(执行异常)'
        return msg,success


    def temperatureDaka(self):
        #体温打卡
        msg=''
        success=False
        try:
            hour = (time.localtime().tm_hour + 8) % 24   # 加8是因为腾讯云跑出来是格林时间，若是运行在自己服务器上需要改回来~
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
                msg=config.stutendID+'体温打卡成功!'
                success=True
            else:
                msg=config.stutendID+'体温打卡失败！请手动完成打卡！'+ '(响应异常)'+str(temperature_response)
        except:
                msg=config.stutendID+'体温打卡失败！请手动完成打卡！'+ '(执行异常)'
        return msg,success

def main_handler(event, context):
    _daka = daka()
    loginMsg = _daka.login()
    healthMsg, healSuc = _daka.healthDaka()
    temperatureMsg, tempSuc = _daka.temperatureDaka()

    if config.sendMsgOnlyError and healSuc and tempSuc:
        pass
    else:
        _daka.sendMsg.sendMessage(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+'\n'+loginMsg+'\n'+healthMsg+'\n'+temperatureMsg)

if __name__ == '__main__':
    main_handler(None,None)
