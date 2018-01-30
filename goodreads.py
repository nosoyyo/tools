#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from quickstart import *

# init mongo
m = MongoDBPipeline()
m.switch('corpus', 'goodreads')

# init soup
headers = {}
headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
headers['Accept-Encoding'] = 'gzip, deflate, br'
headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,es;q=0.6,it;q=0.5'
headers['Cache-Control'] = 'max-age=0'
headers['Connection'] = 'keep-alive'
headers['Cookie'] = 'csid=BAhJIhgyNDAtOTM5MDUwMi04ODQzNzc0BjoGRVQ%3D--a2063c537336ca87f3014923db6a4d1462e7f3d5; locale=zh; __utmc=250562704; csm-sid=772-6969061-9595138; __qca=P0-712970770-1517130738398; __gads=ID=f18481ea47f9593c:T=1517130739:S=ALNI_MZMCTvfwent4PhzlsWlH9Q8kka4qA; _session_id2=80205abf9beea84af6ebb2884ab53693; __utma=250562704.115341626.1517130735.1517172739.1517332300.4; __utmz=250562704.1517332300.4.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; __utmb=250562704.3.10.1517332300'
headers['Host'] = 'www.goodreads.com'
headers['If-None-Match'] = 'W/"f5120950b69079da50a9607f49285fb0"'
headers['Referer'] = 'https://www.goodreads.com/quotes/tag/literature'
headers['Upgrade-Insecure-Requests'] = '1'

url = 'https://www.goodreads.com/quotes/tag/literature?page='

# check if 30 quote divs
def checkSoup(soup):
	if len(soup.select('div.quoteDetails')) == 30:
		print('soup seems alright!')
	else:
		print('soup less than 30, not sure if its still good.')

# quote text content
def getContent(soup, i):
	content = soup.select('div.quoteDetails')[i].div.next.strip()
	return content

# quote author
def getAuthorOrTitle(soup, i):
	author = soup.select('div.quoteDetails')[i].div.a.next
	title_span = soup.select('div.quoteDetails')[i].div.span
	if type(title_span) is not type(None):
		return [author, title_span.text.strip()]
	# when there's authorOrTitle
	else:
		return author

def main(start_page):

	# main loop
	for i in range(start_page, 2854):

		print('now crawling page ' + str(i))

		# check if exists
		if m.col.find({'item_id': i*30}).count() == 0:

			# init item_id
			#item_id = m.col.find().sort('item_id',-1)[0]['item_id'] + 1
			item_id = (i - 1)*30 + 1

			# cook
			url = 'https://www.goodreads.com/quotes/tag/literature?page=' + str(i)
			soup = cookSoup(url, headers=headers)
			checkSoup(soup)

			# grab stuff
			contents = soup.select('div.quoteDetails')

			# retrive content within 30 contents
			for j in range(0, len(contents)):
				# set the anchor
				m.col.insert({'item_id' : item_id})

				content = getContent(soup, j)

				# if title
				if type(getAuthorOrTitle(soup, j)) == type(list()):
					author = getAuthorOrTitle(soup, j)[0]
					title = getAuthorOrTitle(soup, j)[1]
					m.col.update({'item_id': item_id}, {'Content' : content, 'Author' : author, 'Title' : title})

					# post work status update
					print('item_id ' + str(item_id) + ' updated.')
					item_id += 1
					j += 1
				else:
					author = getAuthorOrTitle(soup, j)
					m.col.update({'item_id': item_id}, {'Content' : content, 'Author' : author})

					# post work status update
					print('item_id ' + str(item_id) + ' updated.')
					item_id += 1
					j += 1
			
			# take a nap
			print('page ' + str(i) + ' everything done. now take a nap')
			boringWait(round(random.random()*10+5))

		else:
			print('item_id ' + str(m.col.find({'Content':content})[0]['item_id']) + ' already exsits')
	
		i += 1

if __name__ == '__main__':
	main(1)