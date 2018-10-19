# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2018/10/12'
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
from numpy.random import random_integers
from numpy.random import randn
import numpy as np
import timeit
import argparse
import multiprocessing as mp
import matplotlib.pyplot as plt

def simulate(size):
    n=0
    mean = 0
    M2 = 0
    
    speed = randn(10000)
    for i in range(1000):
        n = n+1
        indices = random_integers(0,len(speed)-1,size=size)
        x = (1+speed[indices]).prod()
        delta = x -mean
        mean = mean + delta/n
        M2 = M2 +delta*(x-mean)
    return mean

def serial():
    start  = timeit.default_timer()
    for i in range(10,50):
        simulate(i)
        
    end = timeit.default_timer()-start
    print("Serial time",end)
    return end

def parallel(nprocs):
    start = timeit.default_timer()
    p = mp.Pool(nprocs,'Pool Create time :{}'.format(timeit.default_timer()-start))
    p.map(simulate,[i for i in range(10,50)])
    print()
    p.close()
    p.join()
    end = timeit.default_timer()-start
    print(nprocs,'Parallel time : {}'.format(end))
    return end


if __name__ == '__main__':
    rations = []
    baseline = serial()
    for i in range(1,mp.cpu_count()):
        rations.append(baseline/parallel(i))
        
    plt.xlabel('# process')
    plt.ylabel('Serial/Parallel')
    plt.plot(np.arange(1,mp.cpu_count()),rations)
    plt.grid(True)
    plt.show()
