# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2018/11/15'
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
import csv
import json
import random
import time
from pprint import pprint

import requests


ua = ['Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
      'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0a1) Gecko/20110623 Firefox/7.0a1 Fennec/7.0a1',
      'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
      'Mozilla/5.0 (Linux; U; Android 4.2.2; zh-cn; LG-D802 Build/JDQ39B) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.2 Mobile Safari/534.30',
      'Mozilla/5.0 (Linux; U; Android 4.2.2; zh-cn; DKL01 Build/DKL01) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
      'Mozilla/5.0 (Linux; U; Android 2.3.6; zh-cn; HUAWEI Y320-U01 Build/HUAWEIY320-U01) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1']


headers = {
    'User-Agent': random.choice(ua),
    # 'Cookie': "_buuid=3a84b621-e09a-4276-875a-f04e1c414f58; session=eyJ1IjoiMjA5NDQ5MDc1Iiwic2VjcmV0IjoiM3BGRzBadG5QNTRoNkhmUUU1LTZJN1liIiwibWlkNDU2ODc2MCI6ZmFsc2UsIl9leHBpcmUiOjE1NDIzNDkyMTgyMjcsIl9tYXhBZ2UiOjg2NDAwMDAwfQ==; session.sig=0qgqMcP7fPuhCduLZRA9Q1TIqXw; global_info={\"from_page\":\"taoumaimai://page?name\u003dcom.taou.maimai.fragment.WebViewFragment\u0026uuid\u003de7262af5-e565-4ef7-b578-d3a4b7322330\u0026url\u003dhttps%3A%2F%2Fmaimai.cn%2Fuh_memlist%3Ffr%3Dvisit_history_hide_setting\",\"launch_uuid\":\"d5bfbafc-6b36-42ec-a3ae-1111e8062cf4\",\"session_uuid\":\"c6432221-b753-42e9-994b-5870deaaaafc\",\"src_page\":\"taoumaimai://page?name\u003dcom.taou.maimai.fragment.WebViewFragment\u0026uuid\u003de7262af5-e565-4ef7-b578-d3a4b7322330\u0026url\u003dhttps%3A%2F%2Fmaimai.cn%2Fuh_memlist%3Ffr%3Dvisit_history_hide_setting\",\"to_page\":\"taoumaimai://page?name\u003dcom.taou.maimai.fragment.WebViewFragment\u0026uuid\u003de7262af5-e565-4ef7-b578-d3a4b7322330\u0026url\u003dhttps%3A%2F%2Fmaimai.cn%2Fuh_memlist%3Ffr%3Dvisit_history_hide_setting\",\"udid\":\"b1d357be-8f0e-4384-bacc-ee19ff0319d2\"}; maimai_u=209449075; maimai_access_token=1.5440fb99b6e4d115e9cd764c9e9edc59; maimai_version=4.23.76; u=209449075; access_token=1.5440fb99b6e4d115e9cd764c9e9edc59; version=4.23.76; channel=huawei",
    # 'Referer': "https://maimai.cn/contact/new_dist2_list?count=6469",
    }
class MaimaiSpider():
    def __init__(self):
        self.headers = headers
    
    def write_data(self,self_info):
        with open('users_rec.csv', 'a', encoding='utf8') as csvFile:
            fieldnames = [key for key in self_info.keys()]
            print(fieldnames)
            # f.write(self_info)
            csvWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
            csvWriter.writerow(self_info)
    
    
    def save_resource(self,html):
        timestamp = time.localtime()
        now_time = time.strftime('%Y%m%d%H%M%S', timestamp)
        with open('{}.txt'.format(now_time),'w') as f:
            f.write(json.dumps(html))
    
    def get_json(self,page):
        explore_url = 'https://maimai.cn/sdk/contact/explore_load_more?page={}&count=10&type=major&channel=huawei&u=209449075&version=4.23.76'
        print(explore_url)
        resp = requests.get(explore_url.format(str(page)),headers=headers)
        html = json.loads(resp.text)
        print(html)
        self.save_resource(html)
        status = html.get('result')
        users = []
        if status == 'ok':
            # print(html)
            data = html.get('data')
            # print(data)
            more = data.get('more')
            print(more)
            cards = data.get('cards')
            # print(cards)
            for item in cards:
                card = item.get('card')
                mmid = card.get('mmid')
                name = card.get('name')
                company = card.get('company')
                short_compos = card.get('short_compos')
                gender = card.get('gender')
                province = card.get('province')
                city = card.get('city')
                position = card.get('position')
                label = card.get('line4')
                figure = card.get('figure')
                encode_mmid = card.get('encode_mmid')
                judge = card.get('judge')  #是否认证
                major = card.get('major')
                dist = card.get('dist')
                rank = card.get('rank')
                is_addr = card.get('is_addr')
                mem_id = card.get('mem_id')
                utype = card.get('utype')
                lv = card.get('lv')
                mem_raw_st = card.get('mem_raw_st')
                emobile = card.get('emobile')
                former = card.get('former')
                qp= card.get('qp')
                avatar = card.get('avatar_large')
                cmf = card.get('cmf')
                dltype = card.get('d1type')
                loc = card.get('loc')
                pub = card.get('pub')
                ouid = card.get('ouid')
                career = card.get('career')
                sr = card.get('sr')
                
                user = dict(
                    mmid=mmid,
                    name=name,
                    company=company,
                    short_compos=short_compos,
                    gender=gender,
                    figure = figure,
                    province=province,
                    city=city,
                    position=position,
                    label=label,
                    encode_mmid=encode_mmid,
                    judge = judge,
                    major=major,
                    dist=dist,
                    rank=rank,
                    is_addr=is_addr,
                    mem_id = mem_id,
                    utype = utype,
                    lv = lv,
                    mem_raw_st = mem_raw_st,
                    emobile = emobile,
                    former = former,
                    qp = qp,
                    avatar = avatar,
                    cmf = cmf,
                    dltype = dltype,
                    loc = loc,
                    pub = pub,
                    ouid = ouid,
                    career = career,
                    sr = sr
                )
                self.write_data(user)
                users.append(user)
            page += 1
            pprint(users)
            if more:
                print("请接着请求")
                self.get_json(page)
            else:
                print("已没有更多！")
                
    def explore_users(self):
        page = 0
        self.get_json(page)
        
    def rec_frs(self):
        page = 0
        url = 'https://maimai.cn/sdk/contact/rec_frs?page={}&count=10&from=nofr_recommend&u=209617155&access_token=1.127229e07329eee27d5f36d6f3331a64&version=4.23.84'
        while True:
            resp = requests.get(url.format(page), headers=self.headers)
            html = json.loads(resp.text)
            self.save_resource(html)
            if html.get('result') == 'ok':
                cards = html.get('contacts')
                for card in cards:
                    mmid = card.get('mmid')
                    name = card.get('name')
                    company = card.get('company')
                    short_compos = card.get('short_compos')
                    gender = card.get('gender')
                    province = card.get('province')
                    city = card.get('city')
                    position = card.get('position')
                    label = card.get('line4')
                    figure = card.get('figure')
                    encode_mmid = card.get('encode_mmid')
                    judge = card.get('judge')  # 是否认证
                    major = card.get('major')
                    dist = card.get('dist')
                    rank = card.get('rank')
                    is_addr = card.get('is_addr')
                    mem_id = card.get('mem_id')
                    utype = card.get('utype')
                    lv = card.get('lv')
                    mem_raw_st = card.get('mem_raw_st')
                    emobile = card.get('emobile')
                    former = card.get('former')
                    qp = card.get('qp')
                    avatar = card.get('avatar_large')
                    cmf = card.get('cmf')
                    dltype = card.get('d1type')
                    loc = card.get('loc')
                    pub = card.get('pub')
                    ouid = card.get('ouid')
                    career = card.get('career')
                    sr = card.get('sr')
    
                    user = dict(
                        mmid=mmid,
                        name=name,
                        company=company,
                        short_compos=short_compos,
                        gender=gender,
                        figure=figure,
                        province=province,
                        city=city,
                        position=position,
                        label=label,
                        encode_mmid=encode_mmid,
                        judge=judge,
                        major=major,
                        dist=dist,
                        rank=rank,
                        is_addr=is_addr,
                        mem_id=mem_id,
                        utype=utype,
                        lv=lv,
                        mem_raw_st=mem_raw_st,
                        emobile=emobile,
                        former=former,
                        qp=qp,
                        avatar=avatar,
                        cmf=cmf,
                        dltype=dltype,
                        loc=loc,
                        pub=pub,
                        ouid=ouid,
                        career=career,
                        sr=sr
                    )
                    self.write_data(user)
                    time.sleep(random.uniform(0.8,3.4))
                page += 1
            else:
                print("已没有更多！")
                break
    def search(self):
        page = 0
        query = '设计'
        url = 'https://maimai.cn/search/fast_contact?count=20&page={}&query={}&dist=3&cid=&company=&forcomp=0&searchTokens=["{}"]&jsononly=1'.format(page,query,query)
        while True:
            resp = requests.get(url.format(page), headers=self.headers)
            html = json.loads(resp.text)
            print(html)
            self.save_resource(html)
            if html.get('result') == 'ok' and html['data']['contacts']:
                cards = html['data'].get('contacts')
                for card in cards:
                    mmid = card.get('mmid')
                    name = card.get('name')
                    company = card.get('company')
                    short_compos = card.get('short_compos')
                    gender = card.get('gender')
                    province = card.get('province')
                    city = card.get('city')
                    position = card.get('position')
                    label = card.get('line4')
                    figure = card.get('figure')
                    encode_mmid = card.get('encode_mmid')
                    judge = card.get('judge')  # 是否认证
                    major = card.get('major')
                    dist = card.get('dist')
                    rank = card.get('rank')
                    is_addr = card.get('is_addr')
                    mem_id = card.get('mem_id')
                    utype = card.get('utype')
                    lv = card.get('lv')
                    mem_raw_st = card.get('mem_raw_st')
                    emobile = card.get('emobile')
                    former = card.get('former')
                    qp = card.get('qp')
                    avatar = card.get('avatar_large')
                    cmf = card.get('cmf')
                    dltype = card.get('d1type')
                    loc = card.get('loc')
                    pub = card.get('pub')
                    ouid = card.get('ouid')
                    career = card.get('career')
                    sr = card.get('sr')
            
                    user = dict(
                        mmid=mmid,
                        name=name,
                        company=company,
                        short_compos=short_compos,
                        gender=gender,
                        figure=figure,
                        province=province,
                        city=city,
                        position=position,
                        label=label,
                        encode_mmid=encode_mmid,
                        judge=judge,
                        major=major,
                        dist=dist,
                        rank=rank,
                        is_addr=is_addr,
                        mem_id=mem_id,
                        utype=utype,
                        lv=lv,
                        mem_raw_st=mem_raw_st,
                        emobile=emobile,
                        former=former,
                        qp=qp,
                        avatar=avatar,
                        cmf=cmf,
                        dltype=dltype,
                        loc=loc,
                        pub=pub,
                        ouid=ouid,
                        career=career,
                        sr=sr
                    )
                    self.write_data(user)
                    time.sleep(random.uniform(0.8, 3.4))
                page += 1
            else:
                print("已没有更多！")
                break
                
        

if __name__ == '__main__':
    maiami = MaimaiSpider()
    maiami.search()