#!/usr/bin/python
# -*- coding: UTF-8 -*-
import web
from schedule.schedule_manager import *
from mail.mail_util import *

# URL 映射
urls = (
    '/hello', 'Hello',
    '/mail', 'Mail',
)

app = web.application(urls, globals())


class Hello:
    def __init__(self):
        pass

    def GET(self):
        return "hello, world!"


class Mail:
    def __init__(self):
        pass

    def GET(self):
        send_mail()

if __name__ == '__main__':
    start_schedule()
    app.run()

