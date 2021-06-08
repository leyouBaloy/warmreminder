import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import re

# #爬取一张好看的图片，此功能未完成
# def get_img_url(keyword):
#     url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + keyword + '&ct=201326592&v=flip'
#     result = requests.get(url)
#     pic_url = re.findall('"objURL":"(.*?)",', result.text, re.S)
#     return str(pic_url[0])



#爬取金句
def get_iciba_everyday():
	url = 'http://open.iciba.com/dsapi/'
	r = requests.get(url)
	return json.loads(r.text)

#爬取毒鸡汤
def get_djt():
    #获取毒鸡汤文案
    url ='https://soul-soup.fe.workers.dev/'
    r = requests.get(url)
    title = r.json()['title']
    return title



#发邮件
def mail(my_sender,my_user,subject,msg_text):
    my_pass = ''  # 请填写开启smtp后产生的密码
    ret = 1
    try:
        msg = MIMEText(msg_text, 'html', 'utf-8')
        msg['From'] = formataddr(["leyouBaloy", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["收件人昵称", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = subject  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = 0
    return ret



def main_handler(event,context):
    #获取金句
    sentence = get_iciba_everyday()
    en = sentence['content']
    zh = sentence['note']

    #获取毒鸡汤
    du = get_djt()

    # #获取图片url
    # img_url = get_img_url(zh)


    my_sender = '1942956063@qq.com'  # 发件人邮箱账号

    #在这里添加收件人信息，key是昵称，value是邮箱号码
    my_user = {'小明':'ilikehhh@163.com',
               }

    subject = '每日金句分享' #主题

    #发送邮件
    ret = []
    for name,mail_num in my_user.items():

        common_msg = f"""
        <body style="margin: 0; padding: 0;" background="https://images.pexels.com/photos/907485/pexels-photo-907485.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940">
            <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse;"> 　
                <tr>
                    <td>
                        <div style="border: #36649d 1px dashed;margin: 30px;padding: 20px"> <label
                                style="font-size: 22px;color: #36649d;font-weight: bold">晚安，{name}</label>
                            <p style="font-size: 16px">今天的金句分享是：&nbsp;<label style="font-weight: bold"> "{en}"</label>&nbsp;
                                翻译是："{zh}" </p>
                            <p style="font-size: 16px">另外，还有一句毒鸡汤："{du}"</p>
                        </div>
                    </td>
                </tr> 　 <tr>
                    <td>
                        <div style="margin: 40px">
                            <p style="font-size: 16px">来自百乐</p>
                            <p style="color:red;font-size: 14px ">（这是一封自动发送的邮件，希望你喜欢。）</p>
                        </div>
                    </td>
                </tr>
                </table>

        """
        tmp = 0
        tmp = mail(my_sender,mail_num,subject,common_msg)
        ret.append(tmp)

    if any(ret):
        return "邮件发送成功"
    else:
        return "邮件发送失败"
