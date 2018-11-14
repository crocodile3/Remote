# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2018/11/14'
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
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'https://y.qq.com/portal/profile.html?uin=ow6qNKcl7K6PNn**#sub=other&tab=fans&'


class Login():
    def __init__(self):
        self.url = "https://y.qq.com/#stat=y_new.top.pop.logout"
        self.brower = webdriver.Chrome("D:/Program Files/Chrome/chromedriver.exe")
        self.wait = WebDriverWait(self.brower, 20)
        self.username = "1140102999@qq.com"
        self.password = "*********"
    
    def login(self):
        """
        返回登录后的cookies
        :return:
        """
        self.brower.get(self.url)
        loginButton = self.wait.until(
            EC.presence_of_element_located((By.XPATH, ".//a[@class='top_login__link js_login']")))
        loginButton.click()
        # 跳转到iframe网页
        self.brower.switch_to.frame("frame_tips")
        pwLogin = self.wait.until(EC.presence_of_element_located((By.ID, 'switcher_plogin')))
        pwLogin.click()
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'u')))
        username.send_keys(self.username)
        pwd = self.wait.until(EC.presence_of_element_located((By.ID, 'p')))
        pwd.send_keys(self.password)
        loginSubmit = self.wait.until(EC.presence_of_element_located((By.ID, 'login_button')))
        loginSubmit.click()
        # 滑块验证
        
        # 获取cookie
        cookies = {}
        self.brower.switch_to.parent_frame()
        time.sleep(1)
        self.brower.get("https://y.qq.com")
        for cookie in self.brower.get_cookies():
            cookies[cookie['name']] = cookie["value"]
        time.sleep(3)
        self.brower.close()
        print("获取cookie成功：{}".format(cookies))
        return cookies
