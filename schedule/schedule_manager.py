# -*- coding:utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
from log import logger
from mail import mail_util
from datebase import sql, loan_after_sql, db_util
from datetime import datetime
import sys
import os


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
    # data['user_id'] = data['user_id'].astype('string')
    # data['id'] = data['id'].astype('string')
    reload(sys)
    sys.setdefaultencoding('utf8')
    now = datetime.now().strftime('%Y%m%d')
    decision_sys_due_pass_name = now + '-决策订单逾期率.xlsx'.encode('utf-8')
    data.to_excel(decision_sys_due_pass_name.decode('utf-8'), sheet_name='Sheet1', index=False,
                  engine='xlsxwriter')

    # 发送邮件
    result = mail_util.attach_mail([decision_sys_due_pass_name, ], to_address, sub, cont)
    # logger.info(result)


def expired_daily():
    # 收件人
    to_address = ['nan.wang@htouhui.com', ]
    # 邮件标题
    sub = '基础数据和决策订单'
    # 邮件内容
    cont = """  
            <html>
                <body>
                    <h1>你好!</h1>
                </body>
            </html>
        """
    # 设置系统编码
    reload(sys)
    sys.setdefaultencoding('utf8')
    now = datetime.now().strftime('%Y%m%d')

    # 每日到期订单
    expired_daily_name = now + '-每日到期订单.xlsx'
    expired_daily_data = db_util.select(loan_after_sql.expired_daily)
    expired_daily_data.to_excel(expired_daily_name, sheet_name='Sheet1', index=False,
                                engine='xlsxwriter')

    # 到期一个月以上
    expired_one_month_more_name = now + '-到期一个月以上.xlsx'
    expired_one_month_more_data = db_util.select(loan_after_sql.expired_one_month_more)
    expired_one_month_more_data.to_excel(expired_one_month_more_name, sheet_name='Sheet1', index=False,
                                         engine='xlsxwriter')

    # 到期
    expired_all_name = now + '-到期.xlsx'
    expired_all_data = db_util.select(loan_after_sql.expired_all)
    expired_all_data.to_excel(expired_all_name, sheet_name='Sheet1', index=False,
                              engine='xlsxwriter')

    # 决策订单逾期率
    decision_sys_due_rate_name = now + '-决策订单逾期率.xlsx'
    decision_sys_due_rate_data = db_util.select(loan_after_sql.decision_sys_due_rate)
    decision_sys_due_rate_data.to_excel(decision_sys_due_rate_name, sheet_name='Sheet1', index=False,
                                        engine='xlsxwriter')

    # 决策订单通过率
    decision_sys_due_pass_name = now + '-决策订单通过率.xlsx'
    decision_sys_due_pass_data = db_util.select(loan_after_sql.decision_sys_pass_rate)
    decision_sys_due_pass_data.to_excel(decision_sys_due_pass_name, sheet_name='Sheet1', index=False,
                                        engine='xlsxwriter')

    # files = [expired_daily_name, expired_one_month_more_name, expired_all_name, decision_sys_due_rate_name,
    #          decision_sys_due_pass_name, ]
    files = [decision_sys_due_rate_name, decision_sys_due_pass_name, ]
    # 发送邮件
    result = mail_util.attach_mail(files, to_address, sub, cont)
    logger.info(result)

    # 删除文件
    # for file in files:
    #     if os.path.exists(file):
    #         os.remove(file)


# 调度定时任务
def start_schedule():
    scheduler = BackgroundScheduler()
    scheduler.add_job(expired_daily, 'interval', minutes=5)
    scheduler.start()


send_mail()
