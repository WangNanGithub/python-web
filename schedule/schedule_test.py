# -*- coding:utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
from log import logger
from datebase import sql, db_util
from mail import mail_test
from util import excel_util
import time
import os


def my_job():
    logger.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


def send_mail():
    to_address = 'nan.wang@htouhui.com'
    sub = '你好'
    cont = '<html><body><h1>你好!</h1></body></html>'
    data = db_util.select(sql.sql)
    data.to_csv(u'D:/用户目录/我的图片/test.csv', index=False, index_label=None)
    base_path = os.getcwd()
    print base_path
    csv_path, xls_path = base_path + 'test.csv', base_path + 'test.xls'
    if os.path.exists(csv_path):
        os.rmdir(csv_path)
    if os.path.exists(xls_path):
        os.rmdir(xls_path)

    excel_util.csv_to_xls(csv_path)
    mail_test.attach_mail([xls_path, ], [to_address, ], sub, cont)


def start_schedule():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(my_job, 'interval', seconds=5)
    scheduler.add_job(send_mail, 'interval', minutes=5)
    scheduler.start()

send_mail()

"""
cron定时调度（某一定时时刻执行）
        (int|str) 表示参数既可以是int类型，也可以是str类型
        (datetime | str) 表示参数既可以是datetime类型，也可以是str类型
         
        year (int|str) – 4-digit year -（表示四位数的年份，如2008年）
        month (int|str) – month (1-12) -（表示取值范围为1-12月）
        day (int|str) – day of the (1-31) -（表示取值范围为1-31日）
        week (int|str) – ISO week (1-53) -（格里历2006年12月31日可以写成2006年-W52-7（扩展形式）或2006W527（紧凑形式））
        day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun) - （表示一周中的第几天，既可以用0-6表示也可以用其英语缩写表示）
        hour (int|str) – hour (0-23) - （表示取值范围为0-23时）
        minute (int|str) – minute (0-59) - （表示取值范围为0-59分）
        second (int|str) – second (0-59) - （表示取值范围为0-59秒）
        start_date (datetime|str) – earliest possible date/time to trigger on (inclusive) - （表示开始时间）
        end_date (datetime|str) – latest possible date/time to trigger on (inclusive) - （表示结束时间）
        timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone) -（表示时区取值）
    --------------------------------------------------------------------------------
    #表示2017年3月22日17时19分07秒执行该程序
    sched.add_job(my_job, 'cron', year=2017,month = 03,day = 22,hour = 17,minute = 19,second = 07)
     
    #表示任务在6,7,8,11,12月份的第三个星期五的00:00,01:00,02:00,03:00 执行该程序
    sched.add_job(my_job, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')
     
    #表示从星期一到星期五5:30（AM）直到2014-05-30 00:00:00
    sched.add_job(my_job(), 'cron', day_of_week='mon-fri', hour=5, minute=30,end_date='2014-05-30')
     
    #表示每5秒执行该程序一次，相当于interval 间隔调度中seconds = 5
    sched.add_job(my_job, 'cron',second = '*/5')
====================================================================================
interval 间隔调度（每隔多久执行）
        weeks (int) – number of weeks to wait
        days (int) – number of days to wait
        hours (int) – number of hours to wait
        minutes (int) – number of minutes to wait
        seconds (int) – number of seconds to wait
        start_date (datetime|str) – starting point for the interval calculation
        end_date (datetime|str) – latest possible date/time to trigger on
        timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations
    --------------------------------------------------------------------------------
    #表示每隔3天17时19分07秒执行一次任务
    sched.add_job(my_job, 'interval',days  = 03,hours = 17,minutes = 19,seconds = 07)
====================================================================================   
date 定时调度（作业只会执行一次）
    # The job will be executed on November 6th, 2009
    sched.add_job(my_job, 'date', run_date=date(2009, 11, 6), args=['text'])
    # The job will be executed on November 6th, 2009 at 16:30:05
    sched.add_job(my_job, 'date', run_date=datetime(2009, 11, 6, 16, 30, 5), args=['text'])
"""