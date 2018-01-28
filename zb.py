#!/usr/bin/env python
# -*- coding: utf-8 -*-

# zhuangbi.info pic crawler
# 2018.1.25

__author__ = 'nosoyyo'

import gc
import time

import pymongo
import requests
from bs4 import BeautifulSoup
from quickstart import boringWait

# init pymongo
client = pymongo.MongoClient("localhost", 27017)
db = client.zhuangbi
col_pic = db['pictures']
col_address = db['address']

# init headers, cookies

headers = {}
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3538.400 QQBrowser/9.6.12501.400'
headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
headers['Accept-Encoding'] = 'gzip, deflate, br'
headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,es;q=0.6,it;q=0.5'
headers['Cache-Control'] = 'max-age=0'
headers['Connection'] = 'keep-alive'
headers['Host'] = 'www.zhuangbi.info'
headers['If-Modified-Since'] = 'Sun, 19 Feb 2017 08:59:20 GMT'
headers['If-None-Match'] = "58a95e68-6bf6"
headers['Referer'] = 'https://www.zhuangbi.info/p/6'
headers['Upgrade-Insecure-Requests'] = '1'

cookies = {}
cookies['Hm_lvt_9bf247c129df7989c3aba11b28931c6e'] = '1516780394'
cookies['Hm_cv_9bf247c129df7989c3aba11b28931c6e'] = '1*user_id*'
cookies['XSRF-TOKEN'] = 'eyJpdiI6InBlUXFjRnhLVmpBekk0Wm1KYWJDU3c9PSIsInZhbHVlIjoibTBuK2dJYnVjejZwd2p4ektkYWk2ZjByXC9sWTVxNEVEdTRxdGc0R1BpSmFuSHQ3NUJmTzJnbXU0VnpGWHJVTFpJZllOdmJhcW4yQXdKc2hnMlFXVEJnPT0iLCJtYWMiOiJiYjAwNTNkNTg1N2FlOTJmY2I2ZGZiMjNkYzM3OTA4ZDEwNThmMDBmZjY1ZjJmNmMwNTBkM2MzMjZjZjdmYzQxIn0%3D;'
cookies['laravel_session'] = 'eyJpdiI6InRnXC9mMFU4R3RDVmM3QnQ2VDJXNHFnPT0iLCJ2YWx1ZSI6InZ2MmVqdVRoMm1uUzdab0h5YlZVYjl3SVVRbVNiUUs1N0t6XC8rZE01UWhQd3NMUmh5bHNUR1RqRkgrQVJGVjg0bzA1djA3T0JycjFxNGpucGRQQk1Fdz09IiwibWFjIjoiZGM5MDBjNWM0ZTM5OGIwMDQ0OWU1ZDlhYmRjYzJhZjRkMWY5MTM0OTYxOTQ5MTlmNTI5MmM4NGE2MGY1MzJjNiJ9'
cookies['Hm_lpvt_9bf247c129df7989c3aba11b28931c6e'] = '1516849381'

class Picture():
	pic_url = ''
	file = 'yeee, no file here'
	desc = ''
	n_combo = ''
	combos = []

# get all available add
def getAddress():
	for i in range(1, 86):

		# init request & soup
		this_url = 'https://zhuangbi.info/?page=' + str(i)
		r = requests.get(this_url, headers = headers, cookies = cookies)
		soup = BeautifulSoup(r.text, "html.parser")

		# get the pic list
		pl = soup.select('div.picture-list')

		# breakpoint
		print('page ' + str(i) + ' ready to go')
		time.sleep(0.1)


		# get pl washed
		for item in pl[1].contents:
			if item == '\n':
				pl[1].contents.remove(item) # now we have a clean pl, len(pl) should be 20
		
		# breakpoint
		print('pl clean & clear!')
		time.sleep(0.1)

		# get available add
		for j in range(0,len(pl[1].contents)):
			p = 'https://zhuangbi.info' + str(pl[1].contents[j].contents[3]).split('"')[3]

			# store in db['address']
			col_address.insert({
				
				"page_id" : p.split('/')[-1]

				})
			j += 1

		# breakpoint
		print('page ' + str(i) + ' done! ' + str(len(pl[1].contents)) + ' addresses stored!')
		time.sleep(0.1)
		
		# breakpoint
		print('now go for page ' + str(i + 1))
		time.sleep(0.1)

		i += 1

	return print('everything in its right place')

# now we have all the available addresses, construct the list
def refreshAddList():
	
	add_list = []
	
	for item in db.address.find():
		num = list(item.values())[-1]
		add_list.append(num)

	return add_list

''' now integrated into quickstart
def boringWait(t):

	for n in range(0, t):
		if t <= 10:
			time.sleep(1)
			print(t - n)
		else:
			if '5' in str(t - n):
				time.sleep(1)
				print(t - n)
			else:
				time.sleep(1)
				print('.', end="")
		n += 1

	return
'''

# normally we run only this
def main():

	# simple stats
	started_at = time.time()

	# bad implementation, keke
	add_list = refreshAddList()
	
	for i in range(0, len(add_list) + 1):

		# check if its already there
		if not col_pic.find({"page_id":add_list[i]}).count():

			# init request & soup
			this_url = 'https://zhuangbi.info/p/' + str(add_list[i])
			r = requests.get(this_url, headers = headers, cookies = cookies)
			soup = BeautifulSoup(r.text, "html.parser")

			# breakpoint
			print('p ' + add_list[i] + ' initialized! wait t secs to fetch pic file')
			
			# countdown
			boringWait(99)

			# get Picture() attrs ready
			p = Picture()
			p.pic_url = str(soup.select('img.image')[0]).split('"')[3]
			p.desc = soup.select('h2')[2].text.strip()
			p.file = requests.get(p.pic_url, headers = headers, cookies = cookies).content
			# init p.combos
			p.combos = []

			# breakpoint
			print('/p/' + add_list[i] + ' pic_url/desc/file ready! wait another 1 sec to go on')
			time.sleep(1)

			# number of combos
			p.n_combos = len(soup.find_all('li')[22:])

			# grab all into combos
			for k in range(0, p.n_combos):
				# why am i so good at dealing with str splits, keke
				p.combos.append(str(soup.find_all('li')[22:][k]).split('"')[3].split('/')[-1])
				k += 1

			# breakpoint
			print('p ' + add_list[i] + ' n_combos ready! it has ' + str(p.n_combos) + ' combos: ' + str(p.combos[:len(p.combos)]))
			time.sleep(0.1)

			# breakpoint
			print('p ' + add_list[i] + ' everything is ready for go!')
			time.sleep(0.1)

			# store stuff into mongodb
			col_pic.insert({

				"page_id" : add_list[i],
				"pic_url" : p.pic_url,
				"file" : p.file,
				"desc" : p.desc,
				"n_combos" : p.n_combos,
				"combos" : p.combos,

				})

			# breakpoint
			print('p ' + add_list[i] + ' everything in its mongodb! wait another t secs')
			print('________________________')
			
			# report stats
			time_usage = time.time() - started_at
			print(str(i) + ' pics grabbed. ' + str(time_usage) + ' secs disappeared forever in your life.')

			# countdown
			boringWait(99)

		else:
			print('page ' + add_list[i] + ' already there, pass!')

	# gc
	gc.collect()

	i += 1

	# report stats
	time_usage = time.time() - started_at
	return print(str(i) + ' pics grabbed. ' + str(time_usage) + ' secs disappeared forever in your life.')

if __name__ == '__main__':
#	getAddress()
	main()
