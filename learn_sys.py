# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2018/10/26'
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
import sys
import os

if len(sys.argv) == 2:
    filename = sys.argv[1]
    print(filename)
    if not os.path.isfile(filename):
        print("[-]"+filename+"  does not exit!")
        exit(0)
    if not os.access(filename,os.R_OK):
        print("[-]"+filename+'  access denied!')
        exit(0)
        
    print("[+] Reading Vulnerabilities From:"+filename)