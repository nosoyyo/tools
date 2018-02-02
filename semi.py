#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'nosoyyo'

import time
import random
import datetime

from pipelines import MongoDBPipeline, WxpyPipeline

# init wx
w = WxpyPipeline()
bot = w.bot

# init pymongo

m = MongoDBPipeline()
profile_col = m.setCol('nosoyyo', 'profile').col
wx_db = 
wx_col = m.setCol('corpus', 'wx').col

# +++++++++++++++++++++++++
# storing wx group messages
# +++++++++++++++++++++++++

# init bot
bot = Bot(cache_path=True, console_qr=True)
bot.enable_puid()

# mao4 pao4
def bubble(type='blah'):
    
    # stochastically speak something nonsense from blahlist
    if type == 'blah':
        
        try:
            blah_col = m.setCol('corpus','wx').col.blah
            blah = random.choice(blah_col.find()[0]['snf'])
            w.staff['snf'].send(blah)

            result = print('blah-blahed\n[' + blah +']\ninto Strangers & Freaks.')
        except Exception as e:
            print(e)

    # a.k.a 'a fallen night', randomly repeat something that was said by others some time ago.
    elif type == 'recurrent':

        try:
            recurrent = 'grab somethin from corpus.wx.puid.asdfasdf'

            result = 'result'
        except Exception as e:
            print(e)

    else:
        print('invalid bubble type')

    return result

def main():

    # this script is only for store wx group messages for now
    @bot.register(Group, except_self=False)
    def storeGroupMessages(msg):

        if msg.sender.puid in list(groups_puid.values()):
            if msg.type == 'Text':
                wx_col.insert({
                    'group' : msg.sender.name,
                    'message_id' : msg.id,
                    'message_type' : msg.type,
                    'content' : msg.text,
                    'create_time' : msg.create_time.ctime(),
                    'sender' : msg.member.name,
                    'sender_puid' : msg.member.puid,
                    })
                print('message \n' + msg + '\n stored!')
            elif msg.type == 'Picture':
                wx_col.insert({
                    'group' : msg.sender.name,
                    'message_id' : msg.id,
                    'message_type' : msg.type,
                    'file_type' : msg.file_name.split('.')[-1],
                    'content' : msg.get_file(),
                    'create_time' : msg.create_time.ctime(),
                    'sender' : msg.member.name,
                    'sender_puid' : msg.member.puid,
                    })
            elif msg.type == 'Sharing':
                wx_col.insert({
                    'group' : msg.sender.name,
                    'message_id' : msg.id,
                    'message_type' : msg.type,
                    'content' : msg.url,
                    'create_time' : msg.create_time.ctime(),
                    'sender' : msg.member.name,
                    'sender_puid' : msg.member.puid,
                    })
            elif msg.type == 'Video':
                wx_col.insert({
                    'group' : msg.sender.name,
                    'message_id' : msg.id,
                    'message_type' : msg.type,
                    'file_type' : msg.file_name.split('.')[-1],
                    'content' : msg.get_file(),
                    'length' : play_length,
                    'create_time' : msg.create_time.ctime(),
                    'sender' : msg.member.name,
                    'sender_puid' : msg.member.puid,
                    })
            elif msg.type == 'Recording':
                wx_col.insert({
                    'group' : msg.sender.name,
                    'message_id' : msg.id,
                    'message_type' : msg.type,
                    'file_type' : msg.file_name.split('.')[-1],
                    'content' : msg.get_file(),
                    'length' : msg.voice_length,
                    'create_time' : msg.create_time.ctime(),
                    'sender' : msg.member.name,
                    'sender_puid' : msg.member.puid,
                    })
            elif msg.type == 'Attachment':
                wx_col.insert({
                    'group' : msg.sender.name,
                    'message_id' : msg.id,
                    'message_type' : msg.type,
                    'file_name' : msg.file_name,
                    'content' : msg.get_file(),
                    'create_time' : msg.create_time.ctime(),
                    'sender' : msg.member.name,
                    'sender_puid' : msg.member.puid,
                    })
            elif msg.type == 'Map':
                wx_col.insert({
                    'group' : msg.sender.name,
                    'message_id' : msg.id,
                    'message_type' : msg.type,
                    'content' : msg.location,
                    'create_time' : msg.create_time.ctime(),
                    'sender' : msg.member.name,
                    'sender_puid' : msg.member.puid,
                    })
        else:
            print(msg + ' ignored')

    print('start listening new messages...')

    # block it up
    bot.join()

# run once every 10 mins
if __name__ == '__main__':
    main()
