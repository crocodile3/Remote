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
from datetime import datetime

import tushare as ts
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# token = 'c873bf443ea91eae100adac4276e978554fdffe0697f93fb4e77bfb8c0efc792'
# pro = ts.pro_api(token)

date = datetime.now().strftime("%Y-%m-%d")
stock_file = 'stock_info' + date + '.csv'


def get_all_stock_info():
    """
    获取所有股票信息
    :return:
    """
    
    data = ts.get_today_all()
    data.to_csv(stock_file)


def get_company_info():
    """
    获取公司上市信息
    :return:
    """


def show_cap():
    np.set_printoptions(suppress=False)
    df = pd.read_csv('stock_info2018-11-01.csv')
    mktcap = df['mktcap']
    print(mktcap.head())
    x = df['code']
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot()
    ax.hist(mktcap)
    plt.show()


if __name__ == '__main__':
    # get_all_stock_info()
    show_cap()
