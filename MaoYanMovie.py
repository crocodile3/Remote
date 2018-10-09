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
from multiprocessing.pool import Pool

import pymysql
import re
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
        self.start_url = "http://maoyan.com/films?showType=2&offset={}"
        self.proxy_url = 'http://127.0.0.1:5555/random'

        # 数据库配置
        self.db_config = {
            "host": "127.0.1.1",
            "database": "spider",
            "user": "root",
            "password": "cyh187977",
            "port": 3306,
            "charset": "utf8"
        }
        self.db = pymysql.connect(**self.db_config)
        self.cursor = self.db.cursor()
        self.headers = {
            "Referer": "http://maoyan.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
        }
    def get_proxy(self):
        try:
            res = requests.get(self.proxy_url)
            print(res.text)
            if res.status_code == 200:
                proxy = res.text
                return proxy
        except Exception as e:
            return None
        
    def get_fake_agent(self):
        ua = UserAgent()
        self.headers['User-Agent'] = ua.random
        return self.headers

    # 构造每个地区的前十页景点的url
    @retry()
    def get_html(self,url):
        headers = self.get_fake_agent()
        # proxy = self.get_proxy()
        # print("本次使用的代理为:{}".format(proxy))
        # proxies = {
        #     'http': 'http://' + proxy,
        #     'https': 'https://' + proxy
        # }
        print("本次请求的地址为：{}".format(url))
        resp = requests.get(url,headers=headers)
        return resp.content.decode()
        
    # 发起请求，获取响应
    def parse_html(self,html):
        pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                             + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                             + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    
        items = re.findall(pattern, html)
        for item in items:
            yield {
                'index': item[0],
                'image': item[1],
                'title': item[2],
                'actor': item[3].strip()[3:],
                'time': item[4].strip()[5:],
                'score': item[5] + item[6]
            }
    
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
    
    def run(self,offset):
        """
        爬虫主逻辑
        :return:
        """
        url = 'http://maoyan.com/board/4?offset=' + str(offset)
        # url = "http://maoyan.com/films?showType=2&offset="+ str(offset)
        html = self.get_html(url)
        for item in self.parse_html(html):
            print(item)


if __name__ == '__main__':
    
    pool = Pool()
    maoyan = MaoYanSpider()
    # pool.map(maoyan.run, [i * 10 for i in range(5)])
    for i in range(10):
        maoyan.run(i*10)
        


