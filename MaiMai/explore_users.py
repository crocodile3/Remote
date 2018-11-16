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
import time
from pprint import pprint

import requests

headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 4.4.2; H60-L01 Build/HDH60-L01) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36/{HUAWEI H60-L01} [Android 4.4.2/19]/MaiMai 4.23.76(1289)",
    'Cookie': "_buuid=3a84b621-e09a-4276-875a-f04e1c414f58; session=eyJ1IjoiMjA5NDQ5MDc1Iiwic2VjcmV0IjoiM3BGRzBadG5QNTRoNkhmUUU1LTZJN1liIiwibWlkNDU2ODc2MCI6ZmFsc2UsIl9leHBpcmUiOjE1NDIzNDkyMTgyMjcsIl9tYXhBZ2UiOjg2NDAwMDAwfQ==; session.sig=0qgqMcP7fPuhCduLZRA9Q1TIqXw; global_info={\"from_page\":\"taoumaimai://page?name\u003dcom.taou.maimai.fragment.WebViewFragment\u0026uuid\u003de7262af5-e565-4ef7-b578-d3a4b7322330\u0026url\u003dhttps%3A%2F%2Fmaimai.cn%2Fuh_memlist%3Ffr%3Dvisit_history_hide_setting\",\"launch_uuid\":\"d5bfbafc-6b36-42ec-a3ae-1111e8062cf4\",\"session_uuid\":\"c6432221-b753-42e9-994b-5870deaaaafc\",\"src_page\":\"taoumaimai://page?name\u003dcom.taou.maimai.fragment.WebViewFragment\u0026uuid\u003de7262af5-e565-4ef7-b578-d3a4b7322330\u0026url\u003dhttps%3A%2F%2Fmaimai.cn%2Fuh_memlist%3Ffr%3Dvisit_history_hide_setting\",\"to_page\":\"taoumaimai://page?name\u003dcom.taou.maimai.fragment.WebViewFragment\u0026uuid\u003de7262af5-e565-4ef7-b578-d3a4b7322330\u0026url\u003dhttps%3A%2F%2Fmaimai.cn%2Fuh_memlist%3Ffr%3Dvisit_history_hide_setting\",\"udid\":\"b1d357be-8f0e-4384-bacc-ee19ff0319d2\"}; maimai_u=209449075; maimai_access_token=1.5440fb99b6e4d115e9cd764c9e9edc59; maimai_version=4.23.76; u=209449075; access_token=1.5440fb99b6e4d115e9cd764c9e9edc59; version=4.23.76; channel=huawei",
    'Referer': "https://maimai.cn/contact/new_dist2_list?count=6469",
    }
class MaimaiSpider():
    def __init__(self):
        self.headers = headers
    
    def write_data(self,self_info):
        with open('users.csv', 'a', encoding='utf8') as csvFile:
            fieldnames = [key for key in self_info.keys()]
            print(fieldnames)
            # f.write(self_info)
            csvWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
            csvWriter.writerow(self_info)
    
    
    def save_resource(self,html):
        timestamp = time.localtime()
        now_time = time.strftime('%Y%m%d%H%M%S', timestamp)
        with open('{}.txt'.format(now_time),'w') as f:
            f.write(html)
    
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
                    encode_mmid=encode_mmid
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
        url = 'https://maimai.cn/sdk/contact/rec_frs?page={}&count=10&from=nofr_recommend&u=209449075&access_token=1.20d5f57dc3d648ce917258a5a4f4bc01&version=4.23.84'
        resp = requests.get(url.format(page),headers=self.headers)
        html = json.loads(resp.text)
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
                
        

if __name__ == '__main__':
    maiami = MaimaiSpider()
    maiami.rec_frs()