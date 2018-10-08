# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2018/10/8'
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

import pymysql
import requests
from lxml import etree
import json
import threading
from queue import Queue

from fake_useragent import UserAgent
# from pymysqlpool import ConnectionPool

from retrying import retry




class MaoYanSpider():
    def __init__(self):
        self.start_url = "http://piao.qunar.com/ticket/list.htm?keyword={}&from=mps_search_suggest&sort=pp&page={}"
        self.proxy_url = 'http://127.0.0.1:5555/random'

        # 数据库配置
        self.db_config = {
            "host": "192.168.85.141",
            "database": "spider",
            "user": "root",
            "password": "mysql",
            "port": 3306,
            "charset": "utf8"
        }
        self.db = pymysql.connect(**self.db_config)
        self.cursor = self.db.cursor()
    
    def get_proxy(self):
        try:
            res = requests.get(self.proxy_url)
            print(res.text)
            if res.status_code == 200:
                proxy = res.text
                return proxy
        except Exception as e:
            return None
    
    # 构造每个地区的前十页景点的url
    def get_html(self):
        # place = input("请输入想搜索的省份：")
        pass

    # 发起请求，获取响应
    def parse_url(self):
        pass

    
    # 3.提取数据
    def get_content_list(self):
        pass
            #
    
    def save_content_dict(self):
        while True:
            # pool = ConnectionPool(**self.db_config)
            # pool.connect()
            
            data = self.content_queue.get()
            keys = ",".join(data.keys())
            values = ",".join(['%s'] * len(data))
            sql = 'insert into %s (%s) values (%s)' % ("spider_qunar", keys, values)
            try:
                self.db.ping(reconnect=True)
                self.cursor.execute(sql, tuple(data.values()))
                self.db.commit()
                print("成功写入数据库")
            except:
                self.db.rollback()
            
            # content_json = json.dumps(data, ensure_ascii=False)
            # with open('qunar.txt', 'a', encoding='utf-8') as f:
            #     f.write(content_json+"\n")
            # print('保存完成一页')
            self.content_queue.task_done()
    
    def run(self):
        """
        爬虫主逻辑
        :return:
        """
        pass


if __name__ == '__main__':
    maoyan = MaoYanSpider()
    maoyan.run()


