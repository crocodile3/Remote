# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2018/10/24'
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

import threading
import time
from queue import Queue


url_queue = Queue()

class MyThread(threading.Thread):
    """
    线程逻辑的主函数
    """
    def __init__(self,func):
        super(MyThread, self).__init__()
        self.func = func
    
    def run(self):
        """
        重写基类的run方法
        :return:
        """
        
def crawl():
    """
    爬虫的主逻辑函数
    :return:
    """
    
def worker():
    """
    主要用来处理工作逻辑，只要队列不为空，就持续处理，
    如果队列为空，检查队列，由于Queue中已经包含了wait，
    notify和锁，所以不需要在取任务的时候加锁或者解锁
    :return:
    """
    global url_queue
    while True:
        if not url_queue.empty():
            item = url_queue.get()
            print("已经拿到任务")
            url_queue.task_done()


def main():
    global url_queue
    threads = []
    for task in range(5):
        url_queue.put(task)
    for i in range(8):
        thread = MyThread(worker)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    url_queue.join()
    
if __name__ == '__main__':
    main()