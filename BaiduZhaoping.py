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
from pprint import pprint

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
        # self.db_config = {
        #     "host": "144.202.81.48",
        #     "database": "spider",
        #     "user": "root",
        #     "password": "187977",
        #     "port": 3306,
        #     "charset": "utf8"
        # }
        # self.db = pymysql.connect(**self.db_config)
        # self.cursor = self.db.cursor()
    
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
    
    def get_detail_url(self,city,keyword,pages):
        url = self.start_url.format(keyword,city,str(pages*10))
        # 更新请求头
        ua = UserAgent()
        self.headers['User-Agent'] = ua.random
        # proxy = self.get_proxy()
        # print("本次使用的代理为:{}".format(proxy))
        # proxies = {
        #     'http': 'http://' + proxy,
        #     'https': 'https://' + proxy
        # }
        try:
            # print("本次使用的代理为:{}".format(proxies))
            res = requests.get(url, headers=self.headers)
            print(res.status_code)
            if res.status_code == 200:
                html_str = res.content.decode()
                # print(html_str)
                data = json.loads(html_str).get("data")
                if data:
                    disp_data = data.get("disp_data")
                    for temp in disp_data:
                        if temp.get("loc"):
                            url = "http://zhaopin.baidu.com/szzw?id="+temp["loc"]
                            yield url
                            
        except Exception as e:
            print("获取url列表失败:{}".format(e))
            with open("fail_url.txt", 'a') as f:
                f.write(url + '\n')


    
    # 发起请求，获取响应
    @retry()
    def parse_url(self,url):
        # 更新请求头
        ua = UserAgent()
        self.headers['User-Agent'] = ua.random
        # proxy = self.get_proxy()
        # print("本次使用的代理为:{}".format(proxy))
        # proxies = {
        #     'http': 'http://' + proxy,
        #     'https': 'https://' + proxy
        # }
        try:
            # print("本次使用的代理为:{}".format(proxies))
            res = requests.get(url, headers=self.headers)
            print(res.status_code)
            html_str = res.content.decode()
            self.get_content_list(html_str)
        except Exception as e:
            print("获取响应失败:{}".format(e))
            with open("fail_url.txt", 'a') as f:
                f.write(url + '\n')
    
    # 3.提取数据
    def get_content_list(self,html_str):
        html = etree.HTML(html_str)
        # 以每个帖子为单元，获取本页中所有的帖子（每个element元素代表一个帖子整体）
        job_name = html.xpath("//h4[@class='job-name']/text()")[0]
        salary = html.xpath("//span[@class='salary']/text()")[0]
        require = html.xpath("//div[@class='job-require']//text()")
        education = require[0]
        expirence = require[1]
        emploee_num = require[2]
        job_class = html.xpath("//p[contains(text(),'职位类型')]/text()")[0].replace("职位类型：","") if html.xpath("//p[contains(text(),'职位类型')]/text()") else None
        release_date = html.xpath("//p[contains(text(),'发布日期')]/text()")[0] if html.xpath("//p[contains(text(),'发布日期')]/text()") else None
        vilid_date = html.xpath("//p[contains(text(),'有效日期')]/text()")[0] if html.xpath("//p[contains(text(),'有效日期')]/text()") else None
        job_place = html.xpath("//p[contains(text(),'工作地点')]/text()")[0]
        job_describe = html.xpath("//div[@class='job-detail']/p/text()")[0]
        job_addr = html.xpath("//div[@class='job-addr']/p[2]/text()")[0]
        gs_name = html.xpath("//div[@class='item-bd']/h4/text()")[0]
        origin = html.xpath("//div[@class='item-bd']/h4/text()")[0]
        job = dict(
            job_name = job_name,
            salary =salary,
            education = education,
            expirence = expirence,
            emploee_num = emploee_num,
            job_class = job_class,
            release_date = release_date,
            vilid_date =vilid_date,
            job_place = job_place,
            job_describe = job_describe,
            job_addr = job_addr,
            gs_name = gs_name,
            origin = origin
        )
        
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
            
            
    def run(self,city,keyword,pages):
        # 1 爬取列表页
        urls = self.get_detail_url(city,keyword,pages)
        # 2 爬取详情页
        for url in urls:
            self.parse_url(url)
        # 3 储存数据
 


if __name__ == '__main__':
    bai = BaiduSpider()
    city = input("请输入要查询的城市：")
    keyword = input("请输入要查询的关键字：")
    jobs_num, pages = bai.get_total(city, keyword)
    print("{}地区共搜索到{}个{}相关职位".format(city, jobs_num, keyword))
    bai.run(city,keyword,1)
    
    



"""
detail_url : http://zhaopin.baidu.com/szzw?id=http://kg.baidu.com/od/4002/2011615/1b1c97a9cef5e2c81d2a5f4698623c7b
"""