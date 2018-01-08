
# coding: utf-8

# In[22]:

# -*- coding: utf-8 -*-
import urllib
import urllib.parse
import urllib.request
import random
import time

import smtplib
from email.mime.text import MIMEText
from email.header import Header


# In[ ]:

# In[23]:

def getToken(email, password):
    url="https://passport.escience.cn/oauth2/authorize"
    #定义要提交的数据    
    postdata = {
        "response_type": "code",
        "redirect_uri": "http://159.226.29.10/CnicCheck/testtoken",        
        "client_id": "58861",
        "theme": "simple",
        "tm": time.time(),
        "pageinfo":"userinfo",
        "userName": email,
        "password": password
    }
    
    #url编码
    postdata=urllib.parse.urlencode(postdata).encode(encoding='UTF8')
    #enable cookie
    request = urllib.request.Request(url,postdata)
    response=urllib.request.urlopen(request)
    # 返回对应的字典
    return eval(response.read())



# In[32]:

def check(userinfo,typeinfo='checkin'):
    '''上班打卡
    '''
    lng = 116.3293553275 + random.random() * 0.001
    lat = 39.9794962420 + random.random() * 0.001
    
#     print(lat,lng)
    
    url="http://159.226.29.10/CnicCheck/CheckServlet"
    postdata = {
        'weidu': lat,
        'jingdu': lng,
        'token': userinfo['token'],
        'refreshToken': userinfo['refreshToken'],
        'uname': userinfo['uname'],
        'uemail': userinfo['uemail'],
        'type': typeinfo
    }
    #url编码
    postdata=urllib.parse.urlencode(postdata).encode(encoding='UTF8')
    #enable cookie
    request = urllib.request.Request(url,postdata)
    response=urllib.request.urlopen(request)
#     print(eval(response.read()))
    return eval(response.read())
    


# In[33]:

def sendEmail(email, password, receiver, typeinfo, ok = 1):
    '''
    寄送email到自己指定的邮箱，收到结果
    sender: 寄送邮箱
    receivers: 接受邮箱
    '''
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    
    sender = "xiaomiao"
    
    subject = "喵喵打卡"

    # 这里需要修改为对应邮箱的服务器
#     smtpserver = "smtp.126.com"
    smtpserver = "mail.cstnet.cn"
    
    email = email
    password = password
    
    txt_start = "喵喵提示:上班打卡成功！"
    txt_end = "喵喵提示:下班打卡成功！"
    
    # 打卡成功
    if ok == 1:
        if typeinfo == 'checkin':
            txt = txt_start
        else:
            txt = txt_end
    else:
        if typeinfo == 'checkin':
            txt = "喵喵提示:上班打卡失败！"
        else:
            txt = "喵喵提示:下班打卡失败！"
    
    
    message = MIMEText(txt, 'plain', 'utf-8')
    message['Subject'] =  Header(subject, 'utf-8')
    message['From'] = 'miaomiao'
    message['To'] = receiver

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver,25)
    smtp.login(email, password)

    smtp.sendmail(email,receiver, message.as_string())
    
    return None



# In[35]:

def run(email, password):
    """run
    
    """
    userinfo = getToken(email, password)
    
    # 上班
    if time.localtime(time.time()).tm_hour < 11:
        result = check(userinfo,'checkin')
        # 打卡时间
        checktime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        
        if result['success'] == 'true':
            print(checktime+" "+ email + ": 上班打卡成功！")
            # 发送邮件
            sendEmail(email,password,email,'checkin', ok=1)
        else:
            print(checktime+" "+ email + ": 上班打卡失败！")
            sendEmail(email,password,email,'checkin', ok=0)
            
            
    # 下班
    if time.localtime(time.time()).tm_hour >= 17:
        result = check(userinfo,'checkout')
        # 打卡时间
        checktime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        
        if result['success'] == 'true':
            print(checktime+" "+ email + ": 下班打卡成功！")
            # 发送邮件
            sendEmail(email,password,email,'checkout', ok=1)
        else:
            print(checktime+" "+ email + ": 下班打卡失败！")
            sendEmail(email,password,email,'checkout', ok=0)
        
    return None

def timefilter():
    '''时间过滤函数，跳过周末和假期
    
    '''
    today_date = time.strftime('%Y%m%d')

    date_file = open('./date/date','r+')
    datelist = []
    for d in date_file.readlines():
        datelist.append(d[:8])
    date_file.close()
    
    # 假期或者周末
    if today_date in datelist:
        return True
    
    return False


def main():
    '''
    主函数运行
    '''
    # 假期或者周末，过滤
    if timefilter():
        print(time.strftime('%Y-%m-%d')+" Today Rest!")
        return None

    # 每一个元素是用户和密码,在这里添加自己的即可
    userlist = [['miaomiao@cnic.cn','miaomiao'],
                ['wangwang@cnic.cn','wangwang']]
    
    # 随机生成一个0-10之间的数字
    delaymin = random.random() * 10
    
    time.sleep(60 * delaymin)    
    
    # 随机打乱，进行打开，每一随机延迟数值秒
    random.shuffle(userlist)

#     print(userlist)
    
    for user in userlist:
        run(user[0],user[1])
        time.sleep(60 * random.random() * 5)
    

# In[ ]:

# run all
main()


