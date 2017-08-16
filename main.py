# -*- coding:utf-8 -*-

import web
from schedule.schedule_test import start_schedule
from mail.mail_test import test

# URL 映射
urls = (
    '/hello', 'hello',
)

app = web.application(urls, globals())


class Hello:
    def __init__(self):
        pass

    def GET(self):
        return "hello, world!"


if __name__ == '__main__':
    test()
    start_schedule()
    app.run()

