#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nosoyyo'

import time
import random

import pymongo
import requests
from wxpy import *
from bs4 import BeautifulSoup

from quickstart import boringWait, MongoDBPipeline, mongodb_init, randomUA

# init pymongo
m = MongoDBPipeline(mongodb_init)
m.switch('fashion', 'tommy')

# init headers
headers = {}
headers['User-Agent'] = randomUA()
headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
headers['Accept-Encoding'] = 'gzip, deflate'
headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,es;q=0.6,it;q=0.5'
headers['Cache-Control'] = 'max-age=0'
headers['Connection'] = 'keep-alive'
headers['Cookie'] = '_ga=GA1.2.818511824.1517175768; _gid=GA1.2.756456048.1517175768'
headers['Host'] = 'www.tommyton.com'
headers['Referer'] = ''
headers['Upgrade-Insecure-Requests'] = '1'

# placeholder
cookies = {}

# started from 1
url='http://www.tommyton.com/?aj=lm&page='

def cookSoup(url=url, headers=headers):

    # get soup ready
    print('[tommyton] getting response from ' + headers['Host'].split(".")[-2].split('//')[-1] + ' ...')
    response = requests.get(url, headers = headers)
    print('[tommyton] got response from ' + headers['Host'].split(".")[-2] + ' . now cooking soup...')
    soup = BeautifulSoup(response.text, "html.parser")

    print('[tommyton] soup ready. enjoy!')
    return soup

xhr = ''

# cook XHR soup
def cookXHRSoup(url=xhr, headers=headers):

    xhr_headers = headers
    xhr_headers['X-Requested-With'] = 'XMLHttpRequest'
    xhr_response = requests.get(url, headers=xhr_headers)
    xhr_soup = BeautifulSoup(xhr_response.text, "html.parser")
    return xhr_soup

# get tags in archive index page
def getTags():
    tags = []

    # get soup
    soup = cookSoup('www.tommyton.com/archive/index.html', headers=headers)

    for i in range(0, len(soup.select('li.lister__item')[5:])):
        tags.append(soup.select('li.lister__item')[5:][i].text.strip())
        i += 1

    # wash
    for i in range(0, len(tags)):
        tags[i] = tags[i].replace('\n×','')
        i += 1

    # quchong
    tags = list(set(tags))

    return tags





# get the a with the sources we want
def getTheA(tag):
    return tag.has_attr('data-overlay-modifier') and tag.has_attr('data-ajax-url') and tag.has_attr('data-overlay-type')

def getTheSpan(tag):
    return tag.has_attr('data-src') and tag.has_attr('data-media')

 # get all the medias, can grab with medias later
def getMediaList(soup):
    media_list = []
    for i in range(0, len(soup(getTheA))):
        media_list.append(soup(getTheA)[i].attrs['href'].replace('#!/media/',''))
    print('media_list ready, ' + str(len(media_list)) + ' medias in the list' )
    return media_list

'''
# get image spans
imgs = list(set(soup(getTheA)[0].div.span.contents))
img_urls = []

# dirty washing
for i in range(0, len(imgs)):
    if 'span' in str(imgs[i]).split(' ')[0]:
        img_urls.append(str(imgs[i]).split(' ')[-1].split('"')[1])
    i += 1
'''
# main
def retrieveMedias(start_at=1):
    try:
        for i in range(start_at,999):
            
            # for pages not visited
            if m.col.find({'Page' : i}).count() == 0:

                # status stating
                print('begin grabbing page ' + str(i))

                # init simple stats
                page_visited = 1
                n_insert = 0
                n_update = 0

                # init page in m.col
                m.col.insert({'Page' : i})
                n_insert +=1

                this_url = url + str(i)
                soup = cookSoup(url=this_url, headers=headers)

                # check soup
                #if some condition:
                #    print('soup is ok')

                # get only this for now
                media_list = getMediaList(soup)

                # store
                for item in media_list:
                    # > 0 means already exists
                    if m.col.find({'Media' : item}).count() > 0:
                        pass
                    else:
                        m.col.insert({'Media' : item})
                        n_insert += 1

                        # breakpoint
                        print(item + ' inserted into m.col')

                # breakpoint
                print('everything done for ' + this_url)
                m.col.update({'Page' : i}, {'Visited' : page_visited})

                # boringWait
                boringWait(60)
            else:

                # status stating
                print('Page + ' + str(i) + ' visited before')

                # for pages visited
                items = m.col.count()
                print('page ' + str(i) + 'already visited')
                print('Collection - ' + m.col.name + ' in database - ' + m.db.name + ' has ' + str(m.col.find({'Page' : i}).count()) + ' items in Page ' + str(i))
                print('Collection - ' + m.col.name + ' has ' + str(items) + ' items in total.')

            # main loop
            i += 1
    
    except Exception as e:
        raise e
    
    finally:
        print('something')

if __name__ == '__main__':
    main(start_at=23)