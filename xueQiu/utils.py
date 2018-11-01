# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2018/11/1'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""


# 数据库操作
import pymysql
from xueQiu.settings import *
from sshtunnel import SSHTunnelForwarder



def open_mysql():
    with SSHTunnelForwarder(
            ('*.*.*.*', 22),  # B机器的配置
            ssh_password='********',
            ssh_username='******',
            remote_bind_address=('127.0.0.1', 3306)) as server:  # A机器的配置
        db = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                             port=server.local_bind_port,
                             user='root',
                             passwd='*******',
                             db='spider')
        cursor = db.cursor()
        return db,cursor




def write_to_mysql(content_dict):
    with SSHTunnelForwarder(
            ('*.*.*.*', 22),  # B机器的配置
            ssh_password='*******',
            ssh_username='*******',
            remote_bind_address=('127.0.0.1', 3306)) as server:  # A机器的配置
        db = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                             port=server.local_bind_port,
                             user='root',
                             passwd='*******',
                             db='spider')
        cursor = db.cursor()
        keys = ",".join(content_dict.keys())
        values = ",".join(['%s'] * len(content_dict))
        sql = 'insert into %s (%s) values (%s)' % ("xueqiu_user", keys, values)
        cursor.execute(sql, tuple(content_dict.values()))
        cursor.close()
        db.commit()
        print("写入完成")

