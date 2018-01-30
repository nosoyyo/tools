#!/usr/bin/env python
# -*- coding: utf-8 -*-

# index
# boringWait() now reads simple lines stochastically
# class MongoDBPipeline()
# class WxpyPipeline()
# randomUA()
# cookSoup()

# todo: boringWait() reads poems while boring waiting
# todo: randomUA add Android, PC etc.
# todo: cookSoup(accept url/headers/cookies as args)

__author__ = 'nosoyyo'

import time
import random

import pymongo
import requests
from wxpy import *
from bs4 import BeautifulSoup

# ===================
# private toys kekeke
# ===================

# when you feel boring sleeping, just call boringWait(t)
def boringWait(t, s="It's very boring, isn't it?"):

    for n in range(0, t):
        if t <= 10:
            time.sleep(1)
            print(t - n)
        else:
            if len(str(t-n)[0:]) > 1 and not str(t-n)[0] == 5:
                time.sleep(1)
                print(t - n)
            else:
                time.sleep(1)
                for m in range(0, round(len(s) / 2)):
                    print(random.choices(s, k=m), end="")
                    m += 1
        n += 1

    return


# ==============
# smtpPipeline()
# ==============

import smtplib


# =================
# Random User-Agent
# =================

def randomUA():
    user_agent_list = [\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36 "
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "  
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",  
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "  
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",  
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "  
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",  
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "  
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",  
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "  
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",  
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "  
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",  
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "  
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",  
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",  
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "  
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",  
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "  
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"  
       ]
    ua = random.choice(user_agent_list)
    return ua

# ==================
# MongoDB quickstart
# ==================

# Initiate MongoDB
mongodb_init = {
            'MONGODB_SERVER' : 'localhost',
            'MONGODB_PORT' : 27017,
            'MONGODB_DB' : 'testdb',
            'MONGODB_COLLECTION' : 'testcol',
            }

class MongoDBPipeline():

    def __init__(self, some_setting_list):

        self.client = pymongo.MongoClient(
            some_setting_list['MONGODB_SERVER'],
            some_setting_list['MONGODB_PORT']
        )
        self.db = self.client.get_database(some_setting_list['MONGODB_DB'])
        self.col = self.db.get_collection(some_setting_list['MONGODB_COLLECTION'])

    def switch(self, db, col):
        self.db = self.client.get_database(db)
        self.col = self.db.get_collection(col)
        return self

# ===============
# wxpy quickstart
# ===============

class WxpyPipeline():

    # init bot
    bot = Bot(cache_path=True, console_qr=True)
    bot.enable_puid()

    staff = {
        'myself' : bot.self,
        'msfc' : bot.groups().search('MSFC')[0],
        'snf' : bot.groups().search('陌生')[0],
        '100k' : bot.groups().search('十万粉')[0],
        'snf_hq' : bot.groups().search('陌怪')[0],
        'sherry' : bot.groups().search('祝雪梨成功')[0],
        'dxns' : bot.groups().search('倒行逆施')[0],
        'sun_palace' : bot.groups().search('太阳宫')[0],
        'change_team' : bot.groups().search('换个新球队')[0],
        }


# ===================================
# Requests + BeautifulSoup quickstart
# ===================================

# init requests with some random headers & cookies 
headers = {}
headers['User-Agent'] = randomUA()

print('[quickstart] User-Agent: ' + headers['User-Agent'])

headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
headers['Accept-Encoding'] = 'gzip, deflate, br'
headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,es;q=0.6,it;q=0.5'
headers['Cache-Control'] = 'max-age=0'
headers['Connection'] = 'keep-alive'
headers['Host'] = ''
headers['If-Modified-Since'] = 'Sun, 19 Feb 2017 08:59:20 GMT'
headers['If-None-Match'] = "58a95e68-6bf6"
headers['Referer'] = 'https://www.apple.com/jobs'
headers['Upgrade-Insecure-Requests'] = '1'

cookies = {}
cookies['Hm_lvt_9bf247c129df7989c3aba11b28931c6e'] = '1516780394'
cookies['Hm_cv_9bf247c129df7989c3aba11b28931c6e'] = '1*user_id*'
cookies['XSRF-TOKEN'] = 'eyJpdiI6InBlUXFjRnhLVmpBekk0Wm1KYWJDU3c9PSIsInZhbHVlIjoibTBuK2dJYnVjejZwd2p4ektkYWk2ZjByXC9sWTVxNEVEdTRxdGc0R1BpSmFuSHQ3NUJmTzJnbXU0VnpGWHJVTFpJZllOdmJhcW4yQXdKc2hnMlFXVEJnPT0iLCJtYWMiOiJiYjAwNTNkNTg1N2FlOTJmY2I2ZGZiMjNkYzM3OTA4ZDEwNThmMDBmZjY1ZjJmNmMwNTBkM2MzMjZjZjdmYzQxIn0%3D;'
cookies['laravel_session'] = 'eyJpdiI6InRnXC9mMFU4R3RDVmM3QnQ2VDJXNHFnPT0iLCJ2YWx1ZSI6InZ2MmVqdVRoMm1uUzdab0h5YlZVYjl3SVVRbVNiUUs1N0t6XC8rZE01UWhQd3NMUmh5bHNUR1RqRkgrQVJGVjg0bzA1djA3T0JycjFxNGpucGRQQk1Fdz09IiwibWFjIjoiZGM5MDBjNWM0ZTM5OGIwMDQ0OWU1ZDlhYmRjYzJhZjRkMWY5MTM0OTYxOTQ5MTlmNTI5MmM4NGE2MGY1MzJjNiJ9'
cookies['Hm_lpvt_9bf247c129df7989c3aba11b28931c6e'] = '1516849381'

# init url
url = ''
cookies = {}

def cookSoup(url, headers=headers, *cookies):

    #headers['Host'] = url
    print('[quickstart] url set to ' + url + '\n')

    # get soup ready
    print('[quickstart] getting response from ' + url.split(".")[-2].split('//')[-1] + ' ...')
    response = requests.get(url, headers = headers, cookies = cookies)
    print('[quickstart] got response from ' + url.split(".")[-2] + ' . now cooking soup...')
    soup = BeautifulSoup(response.text, "html.parser")

    print('[quickstart] soup ready. enjoy!')
    return soup

# cook XHR soup
xhr = ''

def cookXHRSoup(url=xhr, headers=headers, *cookies):

    xhr_headers = headers
    xhr_headers['X-Requested-With'] = 'XMLHttpRequest'
    xhr_response = requests.get(url, headers=xhr_headers)
    xhr_soup = BeautifulSoup(xhr_response.text, "html.parser")
    return xhr_soup

# just for debugging:
def main():

    try:
        testurl = 'http://baidu.com'
        testSoup = cookSoup(testurl)
    except Exception as e:
        raise e
    finally:
        print('test')

    return

if __name__ == '__main__':
    main()