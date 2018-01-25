#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'nosoyyo'

import time
import random
import datetime

from wxpy import *

# init bot
bot = Bot(cache_path=True, console_qr=True)

# init groups
groups = {
	'msfc' : bot.groups().search('MSFC')[0],
	'snf' : bot.groups().search('陌生')[0],
	'snf_hq' : bot.groups().search('陌怪')[0],
	}

# here is the only place you need to add/remove, hopefully
dest_list = [
#			'msfc',
			'snf',
#			'snf_hq'
			]

# debugging construct payload_list
payload_list = [
				'有人怼吗',
				'怼点儿啥',
				'怼啥都行',
				'狗发何在',
				'兴业早',
				'昼夜早',
				'明爷早',
				'撸大师早',
				'各位爷早',
				'没人我一会再来',
				'茬吗',
				'怎么没人理我',
				'那谁在吗',
				'在吗',
				'一波老师早',
				'乐业早',
				'🉐️🉐️早',
				'撕吗',
				'浆液早',
				'兔爷早',
				'土包呢'
				'蛋液早',
				'憨包早',
				'滴液早',
				'俊哉我想你了',
				'银色哮喘爷早',
				'几何老师早',
				]

# Delivery class
class Delivery():
	dest = ''
	payload = ''
#	isPayloadSent = False

	def loadUp(self, payload):
		self.payload = str(payload)
#		isPayloadSent = False
		print('1 payload ready to deliver: \'' + payload +'\'')
		return payload

	'''	
	def unLoad(self):
		payload = ''
		return payload
	'''
	
	# deliver
	def deliver(self, dest):
		self.loadUp(random.choice(payload_list))
		self.dest.send(self.payload)
#		self.isPayloadSent = True
#		self.unLoad()
		return print('Successfully sent 1 payload.')

# construct queue
queue= {}
for i in range(0, len(dest_list)):
	queue[dest_list[i]] = Delivery()
	queue[dest_list[i]].dest = groups[dest_list[i]]
#	queue[dest_list[i]].payload = queue[dest_list[i]].loadUp(random.choice(payload_list))

# run once every 10 mins
if __name__ == '__main__':
	while True:
		if '7' in str(datetime.datetime.now().minute):
			for key in queue:
#				if not queue[key].isPayloadSent:
				queue[key].deliver(queue[key].dest)
				time.sleep(555)