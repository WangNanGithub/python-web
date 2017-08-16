# -*- coding:utf-8 -*-
import logging

# 创建一个logger
logger = logging.getLogger('my-logger')

# 设置日志输出级别
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件
file_handler = logging.FileHandler('export-message.log')
file_handler.setLevel(logging.INFO)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(file_handler)
