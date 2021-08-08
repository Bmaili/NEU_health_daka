### python脚本进行NEU健康、体温打卡，腾讯云定时调用脚本，以防万一，打卡失败时qq邮箱通知。


# 使用流程：

## 1、打卡配置
下载所有文件

在 config.py 文件中填写需要打卡的学号与密码
![1.png](https://z3.ax1x.com/2021/08/08/f1pyTK.png)
## 2、通知邮箱配置（可选）
开启qq邮箱SMTP服务，得到授权码：[参考博客](https://www.cnblogs.com/Alear/p/11594932.html)

在 config.py 文件中配置邮箱信息。
之后可直接运行sendEmail.py文件测试发送效果。

## 3、腾讯云部署
开始部署腾讯云，第一次使用也许你需要实名注册：
[腾讯云Serverless](https://console.cloud.tencent.com/scf/index)


点击函数服务，新建一个云函数：
![2.png](https://z3.ax1x.com/2021/08/08/f1CFVP.md.png)


如图设置：
![3.png](https://z3.ax1x.com/2021/08/08/f1CxoV.md.png)


将修改后的所有文件压缩，然后如图设置，执行方法格式为：文件名+方法名：
![4.png](https://z3.ax1x.com/2021/08/08/f1PyT0.md.png)


上传成功如下，然后点击部署，点击测试，即可立即进行打卡
![5.png](https://z3.ax1x.com/2021/08/08/f1iWUP.md.png)


创建一个自动打卡的定时触发器：选择“自定义触发周期”，cron表达式我是这样写的：11 12 8,13,20 * * * * ，表示每天8点、13点、20点，12分11秒触发函数，即每天三次健康打卡三次体温打卡
![6.png](https://z3.ax1x.com/2021/08/08/f1kiQg.png)


点击“日志查询”可查看之前的日志：
![f1E0Zd.md.png](https://z3.ax1x.com/2021/08/08/f1E0Zd.md.png)

### 完成。通知部分也能用其他的邮箱或者server酱，自动打卡部分也可以挂自己云服务器上或者用git Actions(有时不太稳定)，兄弟们按需修改。
