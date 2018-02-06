#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'nosoyyo'

import time
from datetime import datetime

from wxpy import *
from pipelines import MongoDBPipeline, WxpyPipeline

# init wx
w = WxpyPipeline()
bot = w.bot
w.msfc = {'msfc' : bot.search(puid=w.puid_col.find()[0]['msfc'])}

# init mongo
m = MongoDBPipeline()
blox_col = m.setCol('nosoyyo', 'blox').col
blox = blox_col['blocks']

# init blox
b = Block()
env = []
username = m.col.users.find()[0]['username']
previousBlockId = m.col.blocks.find({},{'id':-1})[0]['id']

taskPool = []

#-----------#
#  classes  #
#-----------#

class Block():
	id = previousBlockId + 1

	def update()

class Task():
	something = 2

class User():
	username = m.col.users.find()[0]['username']
	uuid = 1


#----------#
# commands #
#----------#
def getBlock(id):
	block = m.col.block.find({'id':id})[0]
	return block

def getEnv():
	# are we in block or out
	if 
		isThereActiveBlock = m.col.status.find()[0]['isThereActiveBlock']
		ActiveBlockId = m.col.status.find()[0]['ActiveBlockId']

	env = []

def boc():
	# read db
	# get the newest p_b_id everytime when call boc()
	previousBlockId = m.col.blocks.find({},{'id':-1})[0]['id']
	currentBlockId = previousBlockId + 1
	boc = int(time.time())
	# get previously set stuff

	# operates db
	m.col.blocks.insert({
						'id' : currentBlockId, 
						'boc' : boc,
						})
	m.col.status.update({'status' : 'status'},
						{
						'isThereActiveBlock' : True,
						'ActiveBlockId' : currentBlockId,
		}, True)

	#feedback
	print('<' + username + '>' + ' begins a new block')

	return	


def add(title=None, env=getEnv(), focus=False, ):

	'''
		adding a task,
		- if within an open block, add() adds an active task into current block, not focused by default
		- if not witin an open block, add() adds an 'next' task into 'next'
	'''

	taskPool = getBlock(currentBlockId)['tasks']


	if title == None:
		# print(username + operation)
		opeartion = '添加了一个临时任务'

		# add a task into 'task' anyway
		blox_col['task'].insert({'task_id' : task_id, 'title' : None, 'status' : 0,})
	else:
		opeartion = '开始' + title

		blox_col['task'].insert({'task_id' : task_id, 'title' : None, 'status' : 0,})

	# write into db



def main():



	embed()

if __name__ == '__main__':
	main()