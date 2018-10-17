# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2018/10/16'
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
from pprint import pprint

import re
import requests
import math
import random
# pycrypto
from Crypto.Cipher import AES
import codecs
import base64
import json

from fake_useragent import UserAgent
from retrying import retry


def get_fake_agent():
    ua = UserAgent()
    userAgent = ua.random
    return userAgent


headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
             'Accept-Encoding': 'gzip, deflate',
             'Accept-Language': 'zh-CN,zh;q=0.9',
             'Connection': 'keep-alive',
             'Host': 'music.163.com',
             'Referer': 'http://music.163.com/',
             'Upgrade-Insecure-Requests': '1',
             'User-Agent': get_fake_agent()}

def get_proxy(self):
    try:
        res = requests.get(self.proxy_url)
        print(res.text)
        if res.status_code == 200:
            proxy = res.text
            return proxy
    except Exception as e:
        return None

# 构造函数获取歌手信息
def get_comments_json(url, data):
    
    try:
        # todo 需使用代理
        r = requests.post(url, headers=headers, data=data)
        r.encoding = "utf-8"
        if r.status_code == 200:

            # 返回json格式的数据
            return r.json()

    except:
        print("爬取失败!")


# 生成16个随机字符
def generate_random_strs(length):
    string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    # 控制次数参数i
    i = 0
    # 初始化随机字符串
    random_strs  = ""
    while i < length:
        e = random.random() * len(string)
        # 向下取整
        e = math.floor(e)
        random_strs = random_strs + list(string)[e]
        i = i + 1
    return random_strs


# AES加密
def AESencrypt(msg, key):
    # 如果不是16的倍数则进行填充(paddiing)
    padding = 16 - len(msg) % 16
    # 这里使用padding对应的单字符进行填充
    msg = msg + padding * chr(padding)
    # 用来加密或者解密的初始向量(必须是16位)
    iv = '0102030405060708'

    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 加密后得到的是bytes类型的数据
    encryptedbytes = cipher.encrypt(msg)
    # 使用Base64进行编码,返回byte字符串
    encodestrs = base64.b64encode(encryptedbytes)
    # 对byte字符串按utf-8进行解码
    enctext = encodestrs.decode('utf-8')

    return enctext


# RSA加密
def RSAencrypt(randomstrs, key, f):
    # 随机字符串逆序排列
    string = randomstrs[::-1]
    # 将随机字符串转换成byte类型数据
    text = bytes(string, 'utf-8')
    seckey = int(codecs.encode(text, encoding='hex'), 16)**int(key, 16) % int(f, 16)
    return format(seckey, 'x').zfill(256)


# 获取参数
def get_params(page):
    # msg也可以写成msg = {"offset":"页面偏移量=(页数-1) *　20", "limit":"20"},offset和limit这两个参数必须有(js)
    # limit最大值为100,当设为100时,获取第二页时,默认前一页是20个评论,也就是说第二页最新评论有80个,有20个是第一页显示的
    # msg = '{"rid":"R_SO_4_1302938992","offset":"0","total":"True","limit":"100","csrf_token":""}'
    # 偏移量
    # todo 此处需要根据传入的参数进行判断，是请求哪一个api,然后匹配适合的msg
    offset = (page-1) * 20
    # offset和limit是必选参数,其他参数是可选的,其他参数不影响data数据的生成
    msg = '{"offset":' + str(offset) + ',"total":"True","limit":"20","csrf_token":""}'
    key = '0CoJUm6Qyw8W8jud'
    f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    e = '010001'
    enctext = AESencrypt(msg, key)
    # 生成长度为16的随机字符串
    i = generate_random_strs(16)

    # 两次AES加密之后得到params的值
    encText = AESencrypt(enctext, i)
    # RSA加密之后得到encSecKey的值
    encSecKey = RSAencrypt(i, e, f)
    return encText, encSecKey


# 获取参数
def get_paramsv1(info):
    # msg也可以写成msg = {"offset":"页面偏移量=(页数-1) *　20", "limit":"20"},offset和limit这两个参数必须有(js)
    # limit最大值为100,当设为100时,获取第二页时,默认前一页是20个评论,也就是说第二页最新评论有80个,有20个是第一页显示的
    # msg = '{"rid":"R_SO_4_1302938992","offset":"0","total":"True","limit":"100","csrf_token":""}'
    # 偏移量
    # todo 此处需要根据传入的参数进行判断，是请求哪一个api,然后匹配适合的msg
    """
    top_song <---------------> {offset: "0", total: "true", limit: "60", csrf_token: ""}
    lyric    <---------------> {"id":"483671599","lv":-1,"tv":-1,"csrf_token":""}
    comment  <---------------> {"offset":"0","total":"True","limit":"20","csrf_token":""}
    :param kwargs:
    :return:
    """
    msg = ''
    if info['name'] == 'top_song':
        msg = '{offset: "0", total: "true", limit: "60", csrf_token: ""}'
    elif info['name'] == 'lyric':
        msg = '{"id":"483671599","lv":-1,"tv":-1,"csrf_token":""}'
        # song_id = info['song_id']
        # msg = '{"id":'+song_id+',"lv":-1,"tv":-1,"csrf_token":""}'
    elif info['name'] == 'comment':
        page = info['page']
        offset = (page-1)*20
        msg = '{"offset":'+str(offset)+',"total":"True","limit":"20","csrf_token":""}'
    # offset和limit是必选参数,其他参数是可选的,其他参数不影响data数据的生成
    # msg = '{"offset":' + str(offset) + ',"total":"True","limit":"20","csrf_token":""}'
    # 1 请求热门歌手api
    # 2 请求歌曲歌词api
    # 3 请求歌曲评论的api
    
    key = '0CoJUm6Qyw8W8jud'
    f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    e = '010001'
    enctext = AESencrypt(msg, key)
    # 生成长度为16的随机字符串
    i = generate_random_strs(16)

    # 两次AES加密之后得到params的值
    encText = AESencrypt(enctext, i)
    # RSA加密之后得到encSecKey的值
    encSecKey = RSAencrypt(i, e, f)
    return encText, encSecKey


def hotcomments(html, songname, i, pages, total, filepath):
    # 写入文件
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write("正在获取歌曲{}的第{}页评论,总共有{}页{}条评论！\n".format(songname, i, pages, total))
    print("正在获取歌曲{}的第{}页评论,总共有{}页{}条评论！\n".format(songname, i, pages, total))

    # 精彩评论
    m = 1
    # 键在字典中则返回True, 否则返回False
    if 'hotComments' in html:
        for item in html['hotComments']:
            # 提取发表热门评论的用户名
            user = item['user']
            # 写入文件
            print("热门评论{}: {} : {}    点赞次数: {}".format(m, user['nickname'], item['content'], item['likedCount']))
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write("热门评论{}: {} : {}   点赞次数: {}\n".format(m, user['nickname'], item['content'], item['likedCount']))
                # 回复评论
                if len(item['beReplied']) != 0:
                    for reply in item['beReplied']:
                        # 提取发表回复评论的用户名
                        replyuser = reply['user']
                        print("回复：{} : {}".format(replyuser['nickname'], reply['content']))
                        f.write("回复：{} : {}\n".format(replyuser['nickname'], reply['content']))
            m += 1


def comments(html, songname, i, pages, total, filepath):
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write("\n正在获取歌曲{}的第{}页评论,总共有{}页{}条评论！\n".format(songname, i, pages, total))
    print("\n正在获取歌曲{}的第{}页评论,总共有{}页{}条评论！\n".format(songname, i, pages, total))
    # 全部评论
    j = 1
    for item in html['comments']:
        # 提取发表评论的用户名
        user = item['user']
        print("全部评论{}: {} : {}    点赞次数: {}".format(j, user['nickname'], item['content'], item['likedCount']))
        with open(filepath, 'a', encoding='utf-8') as f:

            f.write("全部评论{}: {} : {}   点赞次数: {}\n".format(j, user['nickname'], item['content'], item['likedCount']))
            # 回复评论
            if len(item['beReplied']) != 0:
                for reply in item['beReplied']:
                    # 提取发表回复评论的用户名
                    replyuser = reply['user']
                    print("回复：{} : {}".format(replyuser['nickname'], reply['content']))
                    f.write("回复：{} : {}\n".format(replyuser['nickname'], reply['content']))

        j += 1


def get_comments(song_infos):
    for song_info in song_infos:
        song_id = song_info[0]
        song_name = song_info[1]

        # 文件存储路径
        filepath = song_name + ".txt"
        page = 1
        info = {'name':'comment','page':page}
        params, encSecKey = get_paramsv1(info)
        print("获取{}的评论".format(song_name))
        url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(song_id) + '?csrf_token='
        data = {'params': params, 'encSecKey': encSecKey}
        # url = 'https://music.163.com/#/song?id=19292984'
        # 获取第一页评论
        html = get_comments_json(url, data)
        # 评论总数
        total = html['total']
        # 总页数
        pages = math.ceil(total / 20)
        hotcomments(html, song_name, page, pages, total, filepath)
        comments(html, song_name, page, pages, total, filepath)
    
        # 开始获取歌曲的全部评论
        page = 2
        while page <= pages:
            info = {'name': 'comment', 'page': page}
            params, encSecKey = get_paramsv1(info)
            data = {'params': params, 'encSecKey': encSecKey}
            html = get_comments_json(url, data)
            # 从第二页开始获取评论
            comments(html, song_name, page, pages, total, filepath)
            page += 1

def get_params_singger():
    offset = 0
    # offset和limit是必选参数,其他参数是可选的,其他参数不影响data数据的生成
    """
    {offset: "0", total: "true", limit: "60", csrf_token: ""}
    """
   
    msg = '{"offset":' + str(offset) + ',"total":"True","limit":"60","csrf_token":""}'
    key = '0CoJUm6Qyw8W8jud'
    f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    e = '010001'
    enctext = AESencrypt(msg, key)
    # 生成长度为16的随机字符串
    i = generate_random_strs(16)
    
    # 两次AES加密之后得到params的值
    encText = AESencrypt(enctext, i)
    # RSA加密之后得到encSecKey的值
    encSecKey = RSAencrypt(i, e, f)
    return encText, encSecKey

# @retry()
def get_singer_list():
    """
    获取歌手列表
    :return:
    url= "https://music.163.com/#/discover/artist/cat?id=1001&initial=65"
    """
    info = {"name":"top_song"}
    params, encSecKey = get_paramsv1(info)
    data = {'params': params, 'encSecKey': encSecKey}
    url = "https://music.163.com/weapi/artist/top?csrf_token="
    res = requests.post(url,headers=headers,data=data)
    artists = json.loads(res.text).get("artists")
    singer_list = []
    for temp in artists:
        singer_id = temp.get("id")
        singer_name = temp.get("name")
        singer_img_url = temp.get("picUrl")
        music_size = temp.get("musicSize")
        singer = dict(
            singer_id=singer_id,
            singer_name=singer_name,
            singer_img_url=singer_img_url,
            music_size = music_size
                    )
        singer_list.append(singer)
    return singer_list

# @retry()
def get_song(singer_id):
    url = "https://music.163.com/artist?id={}".format(singer_id)
    res = requests.get(url,headers=headers)
    html = res.text
    ptn = '<li><a href="\/song\?id=(\d+)">(.*?)<\/a>'
    # 只获取前十首歌曲
    song_info = re.findall(ptn,html,re.I)[:10]
    print("共获取到10首歌：{}".format(song_info))
    return song_info

def save_lyric(name,content):
    path = "lyric/"+name+"txt"
    with open(path,"w") as f:
        f.write(content)

# @retry()
def get_lyrics(song_infos):
    """
    获取歌曲的歌词
    :return:
    data的形式：{"id":"483671599","lv":-1,"tv":-1,"csrf_token":""}
    """
    url = 'https://music.163.com/weapi/song/lyric?csrf_token='
    for song_info in song_infos:
        song_id = song_info[0]
        song_name = song_info[1]
        print("获取{}的歌词".format(song_name))
        info = {"name": "lyric","id":song_id}
        params, encSecKey = get_paramsv1(info)
        data = {'params': params, 'encSecKey': encSecKey}
        res = requests.post(url, headers=headers, data=data)
        lyric = json.loads(res.text).get('lrc').get("lyric")
        # todo 保存歌词
        save_lyric(song_name,lyric)
        
        
def main():
    # 1 获取热门歌手列表
    singer_list = get_singer_list()
    # 2 获取歌手前十位的歌曲
    for singer in singer_list:
        singer_id = singer.get('singer_id')
        print("获取{}的歌单".format(singer['singer_name']))
        song_infos = get_song(singer_id)
        # 获取该歌曲的歌词
        get_lyrics(song_infos)
        # 获取该歌曲的评论
        get_comments(song_infos)


if __name__ == "__main__":
    main()
