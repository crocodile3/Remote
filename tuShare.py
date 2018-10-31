# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2018/10/31'
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
import tushare as ts
token = 'c873bf443ea91eae100adac4276e978554fdffe0697f93fb4e77bfb8c0efc792'
pro = ts.pro_api(token)

def get_all_stock_info():
    """
    获取所有股票信息
    :return:
    """
    data = pro.stock_basic()
    return data

def get_company_info():
    """
    获取公司上市信息
    :return:
    """
    df = pro.stock_company()
    print(df)
    
if __name__ == '__main__':
    get_company_info()