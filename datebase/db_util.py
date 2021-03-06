# -*- coding:utf-8 -*-
import MySQLdb
import numpy as np
import pandas as pd
from config import *
import socket


localIP = socket.gethostbyname(socket.gethostname())  # 得到本地ip
db_info = {}
if localIP == '47.93.157.38' or localIP == '10.29.128.164':
    db_info = db_info_production
elif localIP == '123.57.8.174' or localIP == '10.171.54.98':
    db_info = db_info_test
else:
    db_info = db_info_local


# 获取数据库连接
def open_connection():
    db = MySQLdb.connect(db_info['url'], db_info['username'], db_info['password'], db_info['database'], db_info['port'], charset='utf8')
    return db


# 关闭数据库连接
def close_connection(db):
    db.close()


# 执行SQL语句返回查询结果
def select(sql, db=None):
    flag = False
    try:
        if db is None:
            flag = True
            db = open_connection()
        cursor = db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        pd_df = pd.DataFrame(np.array(data), columns=zip(*cursor.description)[0])
        return pd_df
    finally:
        if flag:
            close_connection(db)


# 插入数据
def insert(sql,  param, db=None):
    flag = False
    try:
        if db is None:
            flag = True
            db = open_connection()
        cursor = db.cursor()
        cursor.execute(sql, param)
        db.commit()
    finally:
        if flag:
            close_connection(db)
