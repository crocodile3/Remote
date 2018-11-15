# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2018/11/11'
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


def get_userid_from_mysql():
    db = pymysql.connect(
        host=MYSQL_HOST,
        database=MYSQL_DATABASE,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        port=MYSQL_PORT,
        charset='utf8'
    )
    cursor = db.cursor()
    
    start_num = 160000
    
    # 总共多少数据
    allData = 4000000
    # 每个批次多少条数据
    dataOfEach = 1000
    # 批次
    while start_num < allData:
        sql = 'select userid from song_comment1 where id >= ' + str(start_num) + ' and id < ' + str(
            start_num + dataOfEach) + ';'
        # print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        start_num += dataOfEach
        yield data
    db.close()
    

def get_self_info(user_id):
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
            place = re.search(r'<span>所在地区：(.*?)</span>',html).group(1) if re.search(r'<span>所在地区：(.*?)</span>',html) else None
            if timeStamp:
                timeStamp = int(timeStamp) / 1000
                date = time.localtime(timeStamp)
                birth = time.strftime('%Y-%m-%d', date)
            else:
                birth = None
            weibo = re.search(r'<a href="(.*?)" class="u-slg u-slg-sn" title="新浪微博"', html).group(1) if ('新浪微博' in html and re.search(r'<a href="(.*?)" class="u-slg u-slg-sn" title="新浪微博"', html)) else None
            douban = re.search(r'<a href="(.*?)" class="u-slg u-slg-db" title="豆瓣网"', html).group(1) if ('豆瓣' in html and re.search(r'<a href="(.*?)" class="u-slg u-slg-db" title="豆瓣网"', html)) else None
            fans = get_followeds(user_id,fan_count)
            follows = get_follows(user_id,follow_count)
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
                douban=douban,
                place = place,
                follows=follows,
                fans=fans
            )
            print(self_info)
            if name is not None:
                with open('user_infoV1.csv','a',encoding='utf8') as csvFile:
                    fieldnames = [key for key in self_info.keys()]
                    print(fieldnames)
                    # f.write(self_info)
                    csvWriter = csv.DictWriter(csvFile,fieldnames=fieldnames)
                    csvWriter.writerow(self_info)
                    redis_client.sadd(user_set,user_id)
                time.sleep(random.uniform(0.3, 1))
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
    followlist = []
    for page in range(pages):
        info = {'name': 'follows', 'page': page, 'uid': userid}
        params, encSecKey = get_paramsv1(info)
        data = {'params': params, 'encSecKey': encSecKey}
        resp = requests.post(follows_url, headers=header, data=data)
        data = json.loads(resp.text)
        follows = data.get('follow')
        if follows:
            for follow in follows:
                follow_dict = {'nickname':follow['nickname'],'useid':follow['userId']}
                followlist.append(follow_dict)
        print('获取第{}页关注人完成'.format(page + 1))
    return followlist


def get_followeds(userid,fan_count):
    """
    获取用户的粉丝列表
    :param userid:
    :return:
    """
    followeds_url = 'https://music.163.com/weapi/user/getfolloweds?csrf_token=e5d4805ff4c96f57d85c1b481b30c121'
    pages = int(fan_count) // 20 + 1
    print('获取{}的粉丝,总计{}页'.format(userid,pages))
    fanslist = []
    for page in range(pages):
        info = {'name': 'followeds', 'page': page, 'uid': userid}
        params, encSecKey = get_paramsv1(info)
        data = {'params': params, 'encSecKey': encSecKey}
        resp = requests.post(followeds_url, headers=header, data=data)
        data = json.loads(resp.text)
        print(data)
        fans = data.get('followeds')
        if fans:
            for fan in fans:
                fan_dict = {'nickname':fan['nickname'],'useid':fan['userId']}
                fanslist.append(fan_dict)
        print('获取第{}页粉丝完成'.format(page+1))
    return fanslist


def get_user_info():
    userid = '375576'
    fan_count = 27
    get_followeds(userid, fan_count)
    # items = get_userid_from_mysql()
    # [get_self_info(userid[0]) for item in items for userid in item]
    

if __name__ == "__main__":
    get_user_info()
