# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2018/11/1'
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
from math import hypot

class vetor:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return 'Vector(%r,%r)' % (self.x,self.y)
    
    def __abs__(self):
        return hypot(self.x,self.y)
    
    def __bool__(self):
        return bool(abs(self))
    
    def __add__(self, other):
        x = self.x+other.x
        y = self.y + other.y
        return Vector(x,y)
    
    def __mul__(self, scalar):
        return Vector(self.x*scalar,self.y*scalar)


v = vetor(2,3)
print(v)