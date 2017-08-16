#!/usr/bin/python
# -*- coding: UTF-8 -*-
import web
from schedule.schedule_test import start_schedule
from mail.mail_test import test

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
        result = test()
        return "mail send : " + result

if __name__ == '__main__':
    test()
    start_schedule()
    app.run()

