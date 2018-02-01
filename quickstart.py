#!/usr/bin/env python
# -*- coding: utf-8 -*-

# index

# class MongoDBPipeline()
# class WxpyPipeline()
# randomUA()
# cookSoup(url, headers=headers, cookies=cookies)
# boringWait(t, m) reads random literature while boring waiting

# todo: checkSoup()
# todo: boringWait() reads poems while boring waiting
# todo: randomUA add Android, PC etc.


__author__ = 'nosoyyo'

import time
import random

import requests
from bs4 import BeautifulSoup

# ===================
# private toys kekeke
# ===================

# when you feel boring sleeping, just call boringWait(t)
def boringWait(t, m, s="It's very boring, isn't it?"):

    #m = MongoDBPipeline()
    m.switch('corpus','goodreads')

    for n in range(0, t):
        if t <= 10:
            time.sleep(1)
            print(t - n)
        else:
            seed = m.col.find({'Author' : 'Milan Kundera'})[2]['Content']
            seed = list(set(seed.split(' '))) + ['love', 'hate', 'wisdom', 'rich',]
            literature = searchQuote(m, random.choice(seed), verbose=False)
            content = random.choice(literature)['Content']
            print(' ' * 8888)
            time.sleep(1)
            print(content)
            time.sleep(9)
            n -= 10

        n += 1

    return

# =============================================================
# goodreads methods, works with m.switch('corpus', 'goodreads')
# ==============================================================

def searchQuote(m, search, verbose=True):

    s = getQuoteByAuthor(m, author=search, show_instance=False, verbose=verbose)
    b = getQuoteByKeyword(m, keyword=search, show_instance=False, verbose=verbose)
    sb = s + b

    if not verbose == False:
        print('\n' + str(len(sb)) + ' item(s) grabbed in total.')

    return sb

def getQuoteByAuthor(m, author='', show_instance=True, verbose=True):
    l = []
    q = []

    # grab all
    for item in m.col.find():
        l.append(item)
    
    if verbose == True:
        print('grabbing "' + author + '" in ' + str(len(l)) + ' items... \n')

    # get content
    for i in range(0, len(l)):
        try:
            if author in l[i]['Author'] or author.capitalize() in l[i]['Author']:
                q.append(l[i])
                i += 1
        except KeyError:
            if verbose == True:
                print('ignoring some KeyError, dont panic')
            else:
                pass
        finally:
            i += 1
    
    if verbose == True:
        print('\n' + str(len(q)) + ' author(s) found. \n')
    
    if show_instance == True and len(q) > 0:
        instance = random.choice(q)
        print('for instance, check this: \n' + instance['Content'] + '\n - ' + instance['Author'])

    return q

def getQuoteByKeyword(m, keyword='', show_instance=True, verbose=True):
    l = []
    q = []

    # grab all
    for item in m.col.find():
        l.append(item)
    
    if verbose == True: 
        print('grabbing "' + keyword + '" in ' + str(len(l)) + ' items... \n')

    # get content
    for i in range(0, len(l)):
        try:
            if keyword in l[i]['Content'] or keyword.capitalize() in l[i]['Content']:
                q.append(l[i])
                i += 1
        except KeyError:
            if verbose == True:
                print('ignoring some KeyError, dont panic')
            else:
                pass
        finally:
            i += 1
    
    if verbose == True:
        print('\n' + str(len(q)) + ' item(s) grabbed within contents. \n')
    
    if show_instance == True and len(q) > 0:
        instance = random.choice(q)
        print('for instance, check this: \n' + instance['Content'] + '\n - ' + instance['Author'])

    return q

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


# ===================================
# Requests + BeautifulSoup quickstart
# ===================================

# init requests with some random headers & cookies 


url = ''
cookies = {}
headers = {}
headers['User-Agent'] = randomUA()

def cookSoup(url, headers=headers, cookies=cookies):

    #headers['Host'] = url
    print('[quickstart] url set to ' + url + '\n')

    # get soup ready
    print('[quickstart] getting response from ' + url.split(".")[-2].split('//')[-1] + ' ...')
    print('started at ' + time.ctime().split()[-2])
    t = time.time()
    response = requests.get(url, headers = headers, cookies = cookies)

    # debug
    response.close()
    
    print('[quickstart] got response from ' + url.split(".")[-2] + ' . now cooking soup...')
    
    soup = BeautifulSoup(response.text, "html.parser")
    print('soup ready in ' + str(int(time.time() - t)) + ' seconds.')
    return soup

# cook XHR soup
xhr = ''

def cookXHRSoup(url=xhr, headers=headers, cookies=cookies):

    xhr_headers = headers
    xhr_headers['X-Requested-With'] = 'XMLHttpRequest'
    xhr_response = requests.get(url, headers=xhr_headers)
    xhr_soup = BeautifulSoup(xhr_response.text, "html.parser")
    return xhr_soup

'''
def soupCheck():


    return
'''

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