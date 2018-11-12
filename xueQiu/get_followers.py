# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2018/11/11'
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

# 读取用户id
# 读取用户的粉丝数
# 获取用户的关注列表
import csv

from wangyiyun import *

userids = ['1498101589', '513258042', '1549421710', '423739995', '1663720871', '439744832', '39060233', '1596909551',
           '529778839', '114007921', '315548893', '256570283', '258687043', '1633658529', '501468999', '426885990',
           '298540359', '93469843', '1309251148', '119831606', '1318121889', '261973902', '555560531', '82457715',
           '1644266755', '471831753', '326120315', '259341498', '321940878', '413079320', '268696430', '487513531',
           '1529191804', '1401311265', '1434631787', '603921389', '302937580', '330234846', '415888263', '517973815',
           '541392244', '614137395', '1663097557', '1627390459', '403807962', '557860163', '403807962', '432040910',
           '432040910', '456325749', '1651553255', '636286579', '1651553255', '1400276373', '579432059', '583592668',
           '1640128878', '444868752', '1640128878', '617525499', '474073318', '133829249', '286949137', '1603226009',
           '1603226009', '432919665', '1291077103', '321132195', '1533456179', '593039915', '1610303789', '323872811',
           '1654945129', '1400276373', '1654945129', '1445067943', '543906644', '1445067943', '317469289', '1663773714',
           '333239342', '1532813737', '1532813737', '435697421', '1486245070', '573777714', '67414702', '606029008',
           '246582102', '378281799', '371996820', '539020159', '621118881', '1400276373', '1400276373', '1400276373',
           '452635366', '1404484656', '292662031', '49186072']


def get_self_info(user_id):
    #todo 做去重判断
    exist_status = redis_client.sismember(user_set,user_id)
    if not exist_status:
        try:
            print('获取{}的信息'.format(user_id))
            url = 'https://music.163.com/user/home?id={}'.format(user_id)
            resp = requests.get(url, headers=header)
            html = resp.text
            name = re.search('<span class="tit f-ff2 s-fc0 f-thide">(.*?)</span>', html).group(1) if re.search('<span class="tit f-ff2 s-fc0 f-thide">(.*?)</span>', html) else None
            level = re.search(r'class="lev u-lev u-icn2 u-icn2-lev">(.*?)<', html).group(1) if re.search(r'class="lev u-lev u-icn2 u-icn2-lev">(.*?)<', html) else None
            event_count = re.search(r'id="event_count">(.*?)<', html).group(1) if re.search(r'id="event_count">(.*?)<', html) else None
            follow_count = re.search(r'id="follow_count">(.*?)<', html).group(1) if re.search(r'id="follow_count">(.*?)<', html) else None
            fan_count = re.search(r'id="fan_count">(.*?)<', html).group(1) if re.search(r'id="fan_count">(.*?)<', html) else None
            self_introduce = re.search(r'个人介绍：(.*?)<', html).group(1) if re.search(r'个人介绍：(.*?)<', html) else None
            timeStamp = re.search(r'data-age="(.*?)">', html).group(1) if re.search(r'data-age="(.*?)">', html) else None
            if timeStamp:
                timeStamp = int(timeStamp) / 1000
                date = time.localtime(timeStamp)
                birth = time.strftime('%Y-%m-%d', date)
            else:
                birth = None
            weibo = re.search(r'<a href="(.*?)" class="u-slg u-slg-sn" title="新浪微博"', html).group(1) if ('新浪微博' in html and re.search(r'<a href="(.*?)" class="u-slg u-slg-sn" title="新浪微博"', html)) else None
            # todo 豆瓣
            douban = ''
            self_info = dict(
                user_id=user_id,
                name=name,
                level=level,
                event_count=event_count,
                follow_count=follow_count,
                fan_count=fan_count,
                self_introduce=self_introduce,
                birth=birth,
                weibo=weibo,
                douban=douban
            )
            with open('user_info.csv','a',encoding='utf8') as csvFile:
                fieldnames = [key for key in self_info.keys()]
                # f.write(self_info)
                csvWriter = csv.DictWriter(csvFile,fieldnames=fieldnames)
                csvWriter.writerow(self_info)
                redis_client.sadd(user_set,user_id)
            time.sleep(random.uniform(0.3, 2))
            return follow_count,fan_count
        except Exception as e:
            with open('fail_users.txt','a') as f:
                f.write(user_id+'\n')

def get_follows(userid,follow_count):
    """
    获取用户的关注列表
    :param userid: 用户id
    :return:
    """
    follows_url = 'https://music.163.com/weapi/user/getfollows/{}?csrf_token=21dc29317636de2e2f6cc8a2dec67d09'.format(
        userid)
    pages = int(follow_count)//20+1
    print('获取{}的关注人,总计{}页'.format(userid, pages))
    for page in range(pages):
        info = {'name': 'follows', 'page': page, 'uid': userid}
        params, encSecKey = get_paramsv1(info)
        data = {'params': params, 'encSecKey': encSecKey}
        resp = requests.post(follows_url, headers=header, data=data)
        data = json.loads(resp.text)
        follows = data.get('follow')
        if follows:
            for follow in follows:
                print(follow)
        print('获取第{}页关注人完成'.format(page + 1))


def get_followeds(userid,fan_count):
    """
    获取用户的粉丝列表
    :param userid:
    :return:
    """
    followeds_url = 'https://music.163.com/weapi/user/getfolloweds?csrf_token=e5d4805ff4c96f57d85c1b481b30c121'
    pages = int(fan_count) // 20 + 1
    print('获取{}的粉丝,总计{}页'.format(userid,pages))
    for page in range(pages):
        info = {'name': 'followeds', 'page': page, 'uid': userid}
        params, encSecKey = get_paramsv1(info)
        data = {'params': params, 'encSecKey': encSecKey}
        resp = requests.post(followeds_url, headers=header, data=data)
        data = json.loads(resp.text)
        fans = data.get('followeds')
        if fans:
            for fan in fans:
                print(fan)
        print('获取第{}页粉丝完成'.format(page+1))


def get_user_info():
    [get_self_info(userid) for userid in userids]
        # 现获取用户信息表（里面有关注数和粉丝数）
        # follow_count,fan_count = get_self_info(userid)
        # 获取关注列表
        # get_follows(userid,follow_count)
        # 获取粉丝列表
        # get_followeds(userid,fan_count)
if __name__ == "__main__":
    get_user_info()
