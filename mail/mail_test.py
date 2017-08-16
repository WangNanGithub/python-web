# -*- coding: utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import smtplib

mail_host = "smtp.mxhichina.com"
mail_username = "hjieqian_statistics@htouhui.com"
mail_password = "htouhui@123"
me = "hello" + "<" + mail_username + ">"


def _format_address(name):
    nickname, address = parseaddr(name)
    return formataddr((Header(nickname, 'utf-8').encode(), address.encode('utf-8') if isinstance(address, unicode) else address))


# 简单文本邮件
def simple_mail(to_list, subject, content):
    msg = MIMEText(content, _subtype='plain', _charset='urf-8')
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    msg['Subject'] = subject
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_username, mail_password)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False


# HTML 邮件
def html_mail(to_list, subject, content):
    msg = MIMEText(content, _subtype='html', _charset='utf-8')  # 创建一个实例，这里设置为html格式邮件
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    msg['Subject'] = subject
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)  # 连接smtp服务器
        s.login(mail_username, mail_password)  # 登陆服务器
        s.sendmail(me, to_list, msg.as_string())  # 发送邮件
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False


# 带附件邮件
def attach_mail(file_list, to_list, subject, content):
    # 创建一个带附件的实例
    msg = MIMEMultipart()
    msg.attach(MIMEText(content, _subtype='plain', _charset='utf-8'))

    # 添加附件
    for attach_file in file_list:
        attachment = MIMEText(open(attach_file, 'rb').read())
        attachment.add_header('Content-Disposition', 'attachment', filename=attach_file.name)
        msg.attach(attachment)

    # 加邮件头
    msg['From'] = me
    msg['To'] = ';'.join(to_list)
    msg['Subject'] = subject

    # 发送邮件
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_username, mail_password)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False


def test():
    to_address = 'nan.wang@htouhui.com'
    sub = '你好'
    cont = '<html><body><h1>你好!</h1></body></html>'
    html_mail([to_address, ], sub, cont)
    simple_mail([to_address, ], sub, cont)

