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

import multiprocessing
import time
from pprint import pprint

import re
import redis
import requests
import random
# pycrypto
import codecs
import base64
import json

import pymysql
from DBUtils.PooledDB import PooledDB

from multiprocessing import Pool
from fake_useragent import UserAgent

#################----MySQL配置----#####################
MYSQL_HOST = "127.0.0.1"
MYSQL_DATABASE = "spider"
MYSQL_USER = "root"
MYSQL_PASSWORD = "cyh187977"
MYSQL_PORT = 3306
#################----MySQL配置----#####################

#################----Redis配置----#####################
redis_config = {
    'host': '127.0.0.1',
    'port': 6379,
    'password': 'spider',
    'decode_responses': True
}
singers_queue = 'singers'
songs_queue = 'songs'
#################----MySQL配置----#####################
redis_client = redis.StrictRedis(**redis_config)


def get_fake_agent():
    ua = UserAgent()
    userAgent = ua.random
    return userAgent

# 请求头设置
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Connection': 'keep-alive',
           'Host': 'xueqiu.com',
           'Referer': 'https://xueqiu.com/people',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': get_fake_agent()}



proxy_url = 'http://127.0.0.1:5555/random'
def get_proxy():
    """
    使用代理
    :return:
    """
    try:
        res = requests.get(proxy_url)
        print(res.text)
        if res.status_code == 200:
            proxy = res.text
            return proxy
    except Exception as e:
        return None
