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
import multiprocessing
import time
from pprint import pprint

import re
import redis
import requests
import math
import random
# pycrypto
from Crypto.Cipher import AES
import codecs
import base64
import json

import pymysql
from DBUtils.PooledDB import PooledDB


from multiprocessing import Pool
from fake_useragent import UserAgent
from retrying import retry

import threading
lock = threading.Lock()
#################----MySQL配置----#####################
MYSQL_HOST = "127.0.0.1"
MYSQL_DATABASE = "spider"
MYSQL_USER = "root"
MYSQL_PASSWORD = "cyh187977"
MYSQL_PORT = 3306
#################----MySQL配置----#####################

#################----Redis配置----#####################
redis_config = {
    'host':'127.0.0.1',
    'port':6379,
    'password':'spider',
    'decode_responses':True
}
singers_queue = 'singers'
songs_queue = 'songs'
#################----MySQL配置----#####################


redis_client = redis.StrictRedis(**redis_config)

def open_mysql():
    global pool
    # pool = ConnectionPool(**config)
    # pool.connect()
    pool = pymysql.connect(
        host=MYSQL_HOST,
        database=MYSQL_DATABASE,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        port=MYSQL_PORT,
        charset='utf8'
    )
    # pool = PooledDB(creator=pymysql,
    #                 maxconnections=20,
    #                 mincached=10,
    #                 maxcached=None,
    #                 blocking=True,
    #                 host=MYSQL_HOST,
    #                 database=MYSQL_DATABASE,
    #                 user=MYSQL_USER,
    #                 password=MYSQL_PASSWORD,
    #                 port=MYSQL_PORT,
    #                 charset='utf8')
    # pool = pool.connection()
    global cursor
    # cursor = pool.cursor(cursor=pymysql.cursors.DictCursor)
    cursor = pool.cursor()


def get_fake_agent():
    ua = UserAgent()
    userAgent = ua.random
    return userAgent


headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Connection': 'keep-alive',
           'Host': 'music.163.com',
           'Referer': 'http://music.163.com/',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': get_fake_agent()}

proxy_url = 'http://127.0.0.1:5555/random'
def get_proxy():
    try:
        res = requests.get(proxy_url)
        print(res.text)
        if res.status_code == 200:
            proxy = res.text
            return proxy
    except Exception as e:
        return None


# 构造函数获取歌手信息
@retry()
def get_comments_json(url, data):
    try:
        # todo 需使用代理
        # proxy = get_proxy()
        # proxies = {
        #     'http': 'http://' + proxy,
        #     'https': 'https://' + proxy
        # }
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
    random_strs = ""
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
    seckey = int(codecs.encode(text, encoding='hex'), 16) ** int(key, 16) % int(f, 16)
    return format(seckey, 'x').zfill(256)


# 获取参数
def get_params(page):
    # msg也可以写成msg = {"offset":"页面偏移量=(页数-1) *　20", "limit":"20"},offset和limit这两个参数必须有(js)
    # limit最大值为100,当设为100时,获取第二页时,默认前一页是20个评论,也就是说第二页最新评论有80个,有20个是第一页显示的
    # msg = '{"rid":"R_SO_4_1302938992","offset":"0","total":"True","limit":"100","csrf_token":""}'
    # 偏移量
    offset = (page - 1) * 20
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
    """
    top_song <---------------> {offset: "0", total: "true", limit: "60", csrf_token: ""}
    lyric    <---------------> {"id":"483671599","lv":-1,"tv":-1,"csrf_token":""}
    comment  <---------------> {"offset":"0","total":"True","limit":"20","csrf_token":""}
    :param kwargs:
    :return:
    """
    msg = ''
    if info['name'] == 'top_song':
        page = info['page']
        offset = page * 60
        msg = '{"offset":' + str(offset) + ', total: "true", limit: "60", csrf_token: ""}'
        print(msg)
    elif info['name'] == 'lyric':
        msg = '{"id":'+info['id']+',"lv":-1,"tv":-1,"csrf_token":""}'
        # song_id = info['song_id']
        # msg = '{"id":'+song_id+',"lv":-1,"tv":-1,"csrf_token":""}'
    elif info['name'] == 'comment':
        page = info['page']
        offset = (page - 1) * 20
        msg = '{"offset":' + str(offset) + ',"total":"True","limit":"20","csrf_token":""}'
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


def hotcomments(html, song_id, songname, i, pages, total, filepath):
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
            # print("热门评论{}: {} : {}    点赞次数: {}".format(m, user['nickname'], item['content'], item['likedCount']))
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write("热门评论{}: {} : {}   点赞次数: {}\n".format(m, user['nickname'], item['content'], item['likedCount']))
                # 回复评论
                if len(item['beReplied']) != 0:
                    for reply in item['beReplied']:
                        # 提取发表回复评论的用户名
                        replyuser = reply['user']
                        # print("回复：{} : {}".format(replyuser['nickname'], reply['content']))
                        f.write("回复：{} : {}\n".format(replyuser['nickname'], reply['content']))
            m += 1


def save_comment(comment_dict):
    keys = ",".join(comment_dict.keys())
    values = ",".join(['%s'] * len(comment_dict))
    sql = 'insert into %s (%s) values (%s)' % ("song_comment", keys, values)
    cursor.execute(sql, tuple(comment_dict.values()))
    pool.commit()


def comments(html, song_id, songname, i, pages, total, filepath):
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write("\n正在获取歌曲{}的第{}页评论,总共有{}页{}条评论！\n".format(songname, i, pages, total))
    print("\n正在获取歌曲{}的第{}页评论,总共有{}页{}条评论！\n".format(songname, i, pages, total))
    # 全部评论
    j = 1
    if html:
        for item in html['comments']:
            # 提取发表评论的用户名
            user = item['user']
            nick_name = user['nickname']
            like_count = item['content']
            timeStamp = item['time']/1000
            date = time.localtime(timeStamp)  # 利用localtime()转换为时间数组
            content = item['content']
            comment_time = time.strftime('%Y-%m-%d %H:%M:%S', date)  # 利用strftime()将其格式化为需要的格式
            # print("全部评论{}: {} : {}    点赞次数: {}".format(j, user['nickname'], item['content'], item['likedCount']))
            
            with open(filepath, 'a', encoding='utf-8') as f:
                
                f.write("全部评论{}: {} : {}   点赞次数: {}\n".format(j, user['nickname'], item['content'], item['likedCount']))
                # 回复评论
                if len(item['beReplied']) != 0:
                    reply_list = []
                    for reply in item['beReplied']:
                        # 提取发表回复评论的用户名
                        replyuser = reply['user']
                        # print("回复：{} : {}".format(replyuser['nickname'], reply['content']))
                        f.write("回复：{} : {}\n".format(replyuser['nickname'], reply['content']))
                        reply = dict(replyuser=replyuser['nickname'], comment=reply['content'])
                        reply_list.append(reply)
                else:
                    reply_list = ""
                    
                
            conment_dict = dict(
                song_id=song_id,
                song_name=songname,
                nick_name=user['nickname'],
                content= content,
                comment_time = comment_time,
                like_count=item["likedCount"],
                reply=str(reply_list))
            save_comment(conment_dict)
            j += 1


def get_comments(song_id,song_name):
    song_id = song_id
    song_name = song_name
    
    # 文件存储路径
    filepath = "comment/" + song_name + ".txt"
    page = 1
    info = {'name': 'comment', 'page': page}
    params, encSecKey = get_paramsv1(info)
    print("获取{}的评论".format(song_name))
    url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(song_id) + '?csrf_token='
    data = {'params': params, 'encSecKey': encSecKey}
    # url = 'https://music.163.com/#/song?id=19292984'
    # 获取第一页评论
    html = get_comments_json(url, data)
    # 评论总数
    if html:
        num = html['total']
        # 总页数

        song_dict = dict(
            song_id=song_id,
            song_name=song_name,
            # singer=singer,
            comment_num=num,
        )
        # print(song_dict)
        save_song_info(song_dict)
        
        pages = math.ceil(num / 20)
        hotcomments(html, song_id, song_name, page, pages, num, filepath)
        comments(html, song_id, song_name, page, pages, num, filepath)
        
        # 开始获取歌曲的全部评论
        page = 2
        while page <= pages:
            info = {'name': 'comment', 'page': page}
            params, encSecKey = get_paramsv1(info)
            data = {'params': params, 'encSecKey': encSecKey}
            html = get_comments_json(url, data)
            # 从第二页开始获取评论
            # comments(html, song_id, song_name, page, pages, num, filepath)
            td = threading.Thread(target=comments,args = (html, song_id, song_name, page, pages, num, filepath))
            td.start()
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
def get_singer_list(page):
    """
    获取歌手列表
    :return:
    url= "https://music.163.com/#/discover/artist/cat?id=1001&initial=65"
    """
    info = {"name": "top_song","page":page}
    params, encSecKey = get_paramsv1(info)
    data = {'params': params, 'encSecKey': encSecKey}
    url = "https://music.163.com/weapi/artist/top?csrf_token="
    # proxy = get_proxy()
    # proxies = {
    #     'http': 'http://' + proxy,
    #     'https': 'https://' + proxy
    # }
    res = requests.post(url, headers=headers, data=data)
    artists = json.loads(res.text).get("artists")
    for temp in artists:
        singer_id = temp.get("id")
        singer_name = temp.get("name")
        singer_img_url = temp.get("picUrl")
        music_size = temp.get("musicSize")
        singer = dict(
            singer_id=singer_id,
            singer_name=singer_name,
            # singer_img_url=singer_img_url,
            # music_size=music_size
        )
        redis_client.rpush(singers_queue,singer)




@retry()
def get_song(singer_id,singer_name):
    
    # try:
    url = "https://music.163.com/artist?id={}".format(singer_id)
    # proxy = get_proxy()
    # proxies = {
    #     'http': 'http://' + proxy,
    #     'https': 'https://' + proxy
    # }
    res = requests.get(url, headers=headers,timeout=30)
    html = res.text
    ptn = '<li><a href="\/song\?id=(\d+)">(.*?)<\/a>'
    # 只获取前十首歌曲
    song_info = re.findall(ptn, html, re.I)
    for song in song_info:
        # song = list(song).append(singer_name)
        # print(song)
        redis_client.rpush(songs_queue,song)
        print("已加入一首歌")
    # except Exception as e:
    #     print("获取{}的歌单失败-{}".format(singer_id,e))
    #     # todo 将失败的歌手信息加入到队列中


def save_lyric(lyric_dict):
    open_mysql()
    # path = "lyric/" + name + ".txt"
    # with open(path, "w") as f:
    #     f.write(content)
    keys = ",".join(lyric_dict.keys())
    values = ",".join(['%s'] * len(lyric_dict))
    sql = 'insert into %s (%s) values (%s)' % ("lyric", keys, values)
    # db.ping(reconnect=True)
    # lock.acquire()
    cursor.execute(sql, tuple(lyric_dict.values()))
    # lock.release()
    pool.commit()
    pool.close()
    
def save_song_info(song_dict):
    open_mysql()
    keys = ",".join(song_dict.keys())
    values = ",".join(['%s'] * len(song_dict))
    sql = 'insert into %s (%s) values (%s)' % ("song_info", keys, values)
    cursor.execute(sql, tuple(song_dict.values()))
    pool.commit()
    



def get_lyrics(song_id,song_name):
    """
    获取歌曲的歌词
    :return:
    data的形式：{"id":"483671599","lv":-1,"tv":-1,"csrf_token":""}
    """
    url = 'https://music.163.com/weapi/song/lyric?csrf_token='
    song_id = song_id
    song_name = song_name
    # singer = singer
    print("获取{}的歌词".format(song_name))
    info = {"name": "lyric", "id": song_id}
    params, encSecKey = get_paramsv1(info)
    data = {'params': params, 'encSecKey': encSecKey}
    # proxy = get_proxy()
    # proxies = {
    #     'http': 'http://' + proxy,
    #     'https': 'https://' + proxy
    # }
  
    res = requests.post(url, headers=headers, data=data)
    lyric_data = json.loads(res.text)
    print("-"*100)
    print(lyric_data)
    print("-" * 100)
    if lyric_data :
        lyric = json.loads(res.text).get('lrc').get("lyric")
        lyric = re.sub(r'(\[.*?\])',"",lyric)
        # # 保存歌曲信息
        # song_dict = dict(
        #     song_id=song_id,
        #     song_name=song_name,
        #     singer=singer,
        #     comment_num=num,
        # )
        # print(song_dict)
        # save_song_info(song_dict)
        # 保存歌词
        lyric_dict = dict(song_id=song_id, song_name=song_name, lyric=lyric)
        print(lyric_dict)
        save_lyric(lyric_dict)
        # except Exception as e:
        #     print("获取{}歌词失败-{}".format(song_name,e))


def main():
   
    # 1 获取热门歌手列表
    # pool = Pool(2)
    # pool.map(get_singer_list,[i for i in range(2) ])
    # pool.close()
    # pool.join()
    # # 2 获取歌单
    # singer_size = redis_client.llen(singers_queue)
    # while singer_size > 0:
    #     for i in range(10):
    #         singer = redis_client.lpop(singers_queue)
    #         if singer:
    #             singer = eval(singer)
    #             singer_id = singer['singer_id']
    #             singer_name = singer['singer_name']
    #             print("获取{}的歌单".format(singer_name))
    #             thread = threading.Thread(target=get_song,args=(singer_id,singer_name))
    #             thread.setDaemon(True)
    #             thread.start()
        # if singer_size ==0:
        #     break
    # 3 获取歌词
    songs_size = redis_client.llen(songs_queue)
    while songs_size > 0:
        for i in range(10):
            songs = redis_client.lpop(songs_queue)
            if songs:
                song = eval(songs)
                song_id = song[0]
                song_name = song[1]
                # thread1 = threading.Thread(target=get_lyrics,args=(song_id,song_name))
                thread2 = threading.Thread(target=get_comments(song_id,song_name))
                # thread1.setDaemon(True)
                # thread1.start()
                # thread1.join()
                thread2.setDaemon(True)
                thread2.start()
                # thread2.join()

            
        
    
        
        
        
        
        
        # for singer in singer_list:
        #     singer_id = singer.get('singer_id')
        #     singer_name = singer['singer_name']
        #     print("获取{}的歌单".format(singer_name))
        #     song_infos = get_song(singer_id)
        #     # 获取该歌曲的歌词
        #     get_lyrics(song_infos, singer_name)
        #     # 获取该歌曲的评论
        #     # get_comments(song_infos,singer_name)
    pool.close()

def get_singer():
    singer = redis_client.lpop(songs_queue)
    print(singer)
    print(type(singer))


if __name__ == "__main__":
    main()
    # get_singer()

