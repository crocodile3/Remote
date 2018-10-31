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
import PyV8
ctxt = PyV8.JSContext()
ctxt.enter()
c = raw_input('请输入验证码:')
add = '''
aesEncrypt = function() {
    var t = CryptoJS.MD5("login.189.cn"),
        i = CryptoJS.enc.Utf8.parse(t),
        r = CryptoJS.enc.Utf8.parse("1234567812345678"),
        u = CryptoJS.AES.encrypt('''+"'{}'".format(c)+''',i, {
            iv: r
        });
    return u + ""
};
'''
with open('crawl_.js')as f:
    a = f.read()
func = ctxt.eval(a + add)
print func()
