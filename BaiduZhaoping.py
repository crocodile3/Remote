# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2018/10/9'
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


class BaiduSpider():
    def __init__(self):
        self.domain = "http://zhaopin.baidu.com/"
        self.start_url = "http://zhaopin.baidu.com/api/qzasync?query={}&city={}&pn={}"
        self.headers = {
            # "Referer": "",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
        }
        self.url_list_queue = Queue() # 保存列表页url
        self.html_list_queue = Queue() # 保存列表页内容
        self.url_queue = Queue()  # 保存url
        self.html_queue = Queue()  # 保存html字符串
        self.content_queue = Queue()  # 保存提取到的数据
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
    
    def get_total(self,city,keyword):
        """
        获取简历总数
        :param city:
        :param keyword:
        :return:
        """
        url = self.start_url.format(keyword,city,str(0))
        resp = requests.get(url=url,headers = self.headers)
        html = json.loads(resp.text)
        data = html.get("data")
        if data:
            jobs_num = data.get("dispNum")
            pages = int(jobs_num)//10+1
            return jobs_num,pages
    
    def get_url_list(self,city,keyword,pages):
        for i in range(pages+1):
            url = self.start_url.format(keyword,city,str(i*10))
            self.url_list_queue.put(url)
    
    
    def get_detail_url(self):
        while True:
            url = self.url_list_queue.get()
            # 更新请求头
            ua = UserAgent()
            self.headers['User-Agent'] = ua.random
            proxy = self.get_proxy()
            print("本次使用的代理为:{}".format(proxy))
            proxies = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy
            }
            try:
                print("本次使用的代理为:{}".format(proxies))
                res = requests.get(url, headers=self.headers, proxies=proxies)
                print(res.status_code)
                html_str = res.content.decode()
                self.html_list_queue.put(html_str)
                self.url_queue.task_done()
            except Exception as e:
                print("获取响应失败:{}".format(e))
                with open("fail_url.txt", 'a') as f:
                    f.write(url + '\n')
    
    
    # 发起请求，获取响应
    @retry()
    def parse_url(self):
        while True:
            url = self.url_queue.get()
            # 更新请求头
            ua = UserAgent()
            self.headers['User-Agent'] = ua.random  # todo 待更换浏览器
            proxy = self.get_proxy()
            print("本次使用的代理为:{}".format(proxy))
            proxies = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy
            }
            try:
                print("本次使用的代理为:{}".format(proxies))
                res = requests.get(url, headers=self.headers, proxies=proxies)
                print(res.status_code)
                html_str = res.content.decode()
                self.html_queue.put(html_str)
                self.url_queue.task_done()
            except Exception as e:
                print("获取响应失败:{}".format(e))
                with open("fail_url.txt", 'a') as f:
                    f.write(url + '\n')
    
    # 3.提取数据
    def get_content_list(self):
        while True:
            html_str = self.html_queue.get()
            html = etree.HTML(html_str)
            # 以每个帖子为单元，获取本页中所有的帖子（每个element元素代表一个帖子整体）
            content_list = []
            # todo 待更新页面解析
            self.html_queue.task_done()
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
        city =  input("请输入要查询的城市：")
        keyword = input("请输入要查询的关键字：")
        jobs_num,pages = self.get_total(city,keyword)
        print("{}地区共搜索到{}个{}相关职位".format(city,jobs_num,keyword))
        self.get_url_list(city,keyword,pages)
        thread_list = []
        for i in range(8):
            # 获取url的线程
            # t_url = threading.Thread(target=self.get_url)
            # thread_list.append(t_url)
            # 发起请求，获取响应的线程
            
            t_parse = threading.Thread(target=self.parse_url)
            thread_list.append(t_parse)
            # 提取数据的线程
            t_get_content = threading.Thread(target=self.get_content_list)
            thread_list.append(t_get_content)
            # 保存数据的线程
            t_save_content = threading.Thread(target=self.save_content_dict)
            thread_list.append(t_save_content)
        
        for t in thread_list:
            # 把子线程设置为守护线程，主进程结束，子线程也会结束
            t.setDaemon(True)
            t.start()
        
        for q in [self.url_queue, self.html_queue, self.content_queue]:
            q.join()
        self.cursor.close()
        self.db.close()


if __name__ == '__main__':
    bai = BaiduSpider()
    bai.run()

