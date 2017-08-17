# -*- coding: utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
from log import logger
from os import path
import smtplib
import mimetypes


mail_host = "smtp.163.com"
mail_username = "wangnan_1001@163.com"
mail_password = "wn19921212"
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
    msg.attach(MIMEText(content, _subtype='html', _charset='utf-8'))

    # 将图片引用到正文
    # msg.attach(MIMEText('<html><body><h1>Hello</h1>'<p><img src="cid:0"></p></body></html>', 'html', 'utf-8'))

    # 添加附件
    for attach_file in file_list:
        with open(attach_file, 'rb') as f:
            mime_type, mime_encoding = mimetypes.guess_type(path.basename(attach_file))
            if (mime_encoding is None) and (mime_type is None):
                mime_type = 'application/octet-stream'

            maintype, subtype = mime_type.split('/', 1)

            mime = MIMEBase(maintype, subtype)
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            mime.add_header('Content-Disposition', 'attachment', filename=path.basename(attach_file))

            # # 将图片引用到正文中时使用
            # mime.add_header('Content-ID', '<0>')
            # mime.add_header('X-Attachment-Id', '0')

            f.close()
            msg.attach(mime)

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
        logger.exception(e)
        return False
