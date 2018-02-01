#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'nosoyyo'

import time
import random

from quickstart import cookSoup, randomUA
from pretommy import headers, getTheSpan
from pipelines import QiniuPipeline, MongoDBPipeline

# init m, q
m = MongoDBPipeline()
m.switch('fashion', 'tommy')
q = QiniuPipeline()

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

cookies = {}
cookies['_ga'] = 'GA1.2.818511824.1517175768'
cookies['_gid'] = 'GA1.2.756456048.1517175768'

# main
def main():
	
	for i in range(0, m.col.media.count()):

		# stating status
		print('now grabbing ' + m.col.media.find()[i]['Media'] + ' ...')

		# check if exists
		if len(m.col.find({'Media' : m.col.media.find()[i]['Media']})[0].keys()) <= 2:
		
			try:	

				url = 'http://www.tommyton.com/media/' + m.col.media.find()[i]['Media']
				soup = cookSoup(url, headers=headers, cookies=cookies)

				# soupCheck, normal == 16
				if len(soup.select('div')) >= 12:
					print('soup seems alright')
				else:
					print('pretty much a 400 Bad Request')

				# get desc if there is one
				if len(soup.select('p.media-module__description')) > 0:
					desc = soup.select('p.media-module__description')[0].text
				else:
					desc = 'No Desccription'
				date = soup.select('p.media-module__date')[0].text

				# stating status
				print(desc + ' | ' + date)

				# get photos
				image_holder = soup.div.div.div.div.div.span
				photo_url_list = []

				try:
					for j in range(0, len(image_holder.find_all('span'))):
						photo_url = image_holder.find_all('span')[j].attrs['data-src']
						photo_url_list.append(photo_url)
				except Exception as e:
					print(e)
				finally:
					# stating status
					print('photo list ready. \n')

					j += 1

				# begin tags part
				tag_wrapper = soup.select('div.story__tags--media')
				tags = []
				try:
					for k in range(0, len(tag_wrapper[0].find_all('a'))):
						tags.append({
							'Tag Name' : tag_wrapper[0].find_all('a')[k].attrs['data-tag_name'],
							'Tag ID' : tag_wrapper[0].find_all('a')[k].attrs['data-tag_id'],
							'Tag Url' : tag_wrapper[0].find_all('a')[k].attrs['href'],
							})
				except Exception as e:
					print(e)
				finally:
					# stating status
					print(str(len(tags)) + ' tags ready. \n')
					for n in range(0, len(tags)):
						print(tags[n]['Tag Name'] + ', ', end='')
					k += 1

				# store
				m.col.update({'Media':m.col.media.find()[i]['Media']},
					{
					'Media' : m.col.media.find()[i]['Media'],
					'Desc' : desc,
					'Date' : date,
					'Photos' : photo_url_list,
					'Tags' : tags,
					})

				# store pic upon Qiniu
				pic_url = photo_url_list[-1]
				ret = q.upload(pic_url)

				if ret[1].ok():
					print(pic_url + ' replicated upon Qiniu \n')
				else:
					print('something might be wrong with ' + pic_url)

				# stating status
				print('\n ' + m.col.media.find()[i]['Media'] + 'stuff updated. \n')
				
			except Exception as e:
				print('~~~~~~~~~~~~~~~~')
				print(e)
				print('~~~~~~~~~~~~~~~~')

			finally:
				print("\n everything's alright, now go for the next in 1 min.")
				print(time.ctime().split()[-2])
				#boringWait(3, m)
				time.sleep(60)

		i += 1


if __name__ == '__main__':

	try:
		main()
	except IndexError:
		print('weird IndexError again')
	finally:
		print('hmmm.....')