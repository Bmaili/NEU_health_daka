![](http://bmalimarkdown.oss-cn-beijing.aliyuncs.com/img/QQ图片20220502013357.jpg)

# 脚本说明

**python（本地无python环境也ok）脚本进行NEU健康、体温打卡，使用腾讯云云函数定时调用脚本，以防万一，打卡失败时将通知使用者。**




# 使用流程

## 个人信息配置

下载所有文件，解压，在 config.py 文件中填写需要打卡的学号与密码

![](http://bmalimarkdown.oss-cn-beijing.aliyuncs.com/img/image-20220502010356041.png)
## 通知配置（可选）

打卡通知设置，相应渠道设置后，将自动推送通知。

- ### 邮箱通知

开启qq邮箱SMTP服务，得到授权码：[参考博客](https://www.cnblogs.com/Alear/p/11594932.html)

在 config.py 文件中配置邮箱信息。之后可直接运行sendEmail.py文件测试发送效果。

- ### Server酱通知

在 config.py 文件中配置Server酱的SCKEY，可以在Server酱的网站注册获取。之后可直接运行sendEmail.py文件测试发送效果。

## 腾讯云部署
#### （自2022年6月1日起腾讯云函数服务不再免费，建议换成[华为云函数工作流](https://console.huaweicloud.com/functiongraph/?region=cn-south-1#/serverless/dashboard)，使用方式与下面相似）

1. 开始部署腾讯云，第一次使用也许你需要实名注册：[~~腾讯云Serverless~~](https://console.cloud.tencent.com/scf/index)     [华为云函数工作流](https://console.huaweicloud.com/functiongraph/?region=cn-south-1#/serverless/dashboard)

2. 点击函数服务，新建一个云函数：

![](http://bmalimarkdown.oss-cn-beijing.aliyuncs.com/img/yun1.png)



3. 自定义函数，注意运行环境是Python3.6：

![](http://bmalimarkdown.oss-cn-beijing.aliyuncs.com/img/yun2.png)



4. 将修改后的所有文件压缩，然后如图设置，执行方法格式为：文件名+方法名：

![](http://bmalimarkdown.oss-cn-beijing.aliyuncs.com/img/yun3.png)



5. 高级配置：环境配置里的执行超时时间不能太小

![](http://bmalimarkdown.oss-cn-beijing.aliyuncs.com/img/yun4.png)



6. 触发器配置：自定义一个定时触发器，cron表达式我是这样写的：11 12 8,13,20 * * * * ，表示每天8点、13点、20点，12分11秒触发函数，即每天三次健康打卡三次体温打卡

   ![](http://bmalimarkdown.oss-cn-beijing.aliyuncs.com/img/yun5.png)

   

7. 点击”完成“进行创建。点击”部署“可再次部署，点击”测试“可立即测试打卡，点击日志查询可查看近期打卡日志。

   ![](http://bmalimarkdown.oss-cn-beijing.aliyuncs.com/img/image-20220502013928983.png)

## 其他

通知部分也能用其他邮箱，自动打卡部分也可以挂自己云服务器上或者用GitHub Actions(偶尔抽风)，兄弟们按需修改（体温打卡因为腾讯云函数跑出来是格林时间，进行了+8处理，若是部署到自己服务器上需要改回来）。
