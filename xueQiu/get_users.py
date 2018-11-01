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

import requests
import json
from requests_html import HTMLSession
from xueQiu.settings import *
from xueQiu.utils import write_to_mysql

def get_first_user(uid=1102105103):
    uid = uid
    start_url = 'https://xueqiu.com/u/{}'.format(uid)
    # get_followers(uid,start_url)
    # get_members(uid,start_url)
    member_url = 'https://xueqiu.com/friendships/groups/members.json?uid={}&page=1&gid=0'.format(uid)
    follower_url = 'https://xueqiu.com/friendships/followers.json?uid={}&pageNo=1'.format(uid)
    get_followers(uid,start_url,follower_url=follower_url,member_url=member_url)


def deal_res(content):
    type = content['type']
    if type == 'member':
        users = content.get('users')
        for user in users:
            uid = user.get('id')
            # get_first_user(uid)
            name = user.get('screen_name')
            description = user.get('description')
            followers_count = user.get('followers_count')
            friends_count = user.get('friends_count')
            verified_description = user.get('verified_description')
            verified = user.get('verified')
            province = user.get('province')
            city = user.get('city')
            stocks_count = user.get('stocks_count')
            cube_count = user.get('cube_count')
            temp = dict(
                uid=uid,
                name=name,
                description=description,
                followers_count=followers_count,
                friends_count=friends_count,
                verified=verified,
                verified_description=verified_description,
                province=province,
                city=city,
                stocks_count=stocks_count,
                cube_count=cube_count
            )
            write_to_mysql(temp)
            print(temp)
    else:
        users = content.get('followers')
        for user in users:
            uid = user.get('id')
            # get_first_user(uid)
            name = user.get('screen_name')
            description = user.get('description')
            followers_count = user.get('followers_count')
            friends_count = user.get('friends_count')
            verified_description = user.get('verified_description')
            verified = user.get('verified')
            province = user.get('province')
            city = user.get('city')
            stocks_count = user.get('stocks_count')
            cube_count = user.get('cube_count')
            temp = dict(
                uid=uid,
                name=name,
                description=description,
                followers_count=followers_count,
                friends_count=friends_count,
                verified=verified,
                verified_description=verified_description,
                province=province,
                city=city,
                stocks_count=stocks_count,
                cube_count=cube_count
            )
            write_to_mysql(temp)

        
def get_followers(uid,start_url,member_url,follower_url):
    """
    粉丝
    :return:
    """
    print(member_url)
    headers['Referer'] = start_url
    headers['Cookie'] = 'device_id=f7ca6434494ddf6be82e95c92a377533; s=e11soc8cis; __utma=1.1884092199.1539853904.1539853904.1539853904.1; __utmz=1.1539853904.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); aliyungf_tc=AQAAAEh1t3nDaQUAwv4R2gBZCA/0D+bg; xq_a_token=088c6ad5e275496d7c91b8b5b2ecb929bee15772; xq_a_token.sig=NcpAm7FRsAVoMGRMOLrLRveBT7U; xq_r_token=08131eb9a4f33b43b2340fd782f3776c9823d74a; xq_r_token.sig=AZ7au6ICJtTgQJVPybkOJs_Fr54; u=791541054821726'
    # 处理关注的人
    if member_url:
        rsp = requests.get(member_url,headers=headers)
        item = json.loads(rsp.text)
        maxPage = item.get('maxPage')
        item['type'] = 'member'
        deal_res(item)
        if maxPage >1:
            for i in range(2,maxPage+1):
                url = 'https://xueqiu.com/friendships/groups/members.json?uid={}&page={}&gid=0'.format(uid,i)
                print(url)
                res = requests.get(url,headers=headers)
                item = json.loads(res.text)
                item['type'] = 'member'
                deal_res(item)
                
    # 处理粉丝
    if follower_url:
        rsp = requests.get(follower_url, headers=headers)
        item = json.loads(rsp.text)
        maxPage = item.get('maxPage')
        print(maxPage)
        item['type'] = 'follower'
        deal_res(item)
        if maxPage > 1:
            for i in range(2, maxPage + 1):
                url = 'https://xueqiu.com/friendships/followers.json?uid={}&pageNo={}'.format(uid, i)
                print(url)
                res = requests.get(url, headers=headers)
                item = json.loads(res.text)
                item['type'] = 'follower'
                deal_res(item)
    
    
if __name__ == '__main__':
    get_first_user()






