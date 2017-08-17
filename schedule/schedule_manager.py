# -*- coding:utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
from log import logger
from mail import mail_util
from datebase import sql, db_util
from datetime import datetime


def send_mail():
    # 收件人
    to_address = ['nan.wang@htouhui.com', ]
    # 邮件标题
    sub = '你好'
    # 邮件内容
    cont = """  
        <html>
            <body>
                <h1>你好!</h1>
            </body>
        </html>
    """

    # 查询数据
    data = db_util.select(sql.sql)
    data['user_id'] = data['user_id'].astype('string')
    data['id'] = data['id'].astype('string')
    data.to_excel(datetime.now().strftime('%Y-%m-%d') + '-data.xls', sheet_name='Sheet1', index=False, engine='xlsxwriter')

    # 发送邮件
    result = mail_util.attach_mail([datetime.now().strftime('%Y-%m-%d') + '-data.xls', ], to_address, sub, cont)
    logger.info(result)


# 调度定时任务
def start_schedule():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mail, 'interval', minutes=5)
    scheduler.start()

send_mail()

