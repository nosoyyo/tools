#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'nosoyyo'

import time
import random
import datetime

from wxpy import *
from pipelines import MongoDBPipeline, WxpyPipeline

# init wx
w = WxpyPipeline()
bot = w.bot
w.staff = {
    'myself' : bot.self,
    'msfc' : bot.search(puid=w.puid_col.find()[0]['msfc']),
    'snf' : bot.search(puid=w.puid_col.find()[0]['snf']),
    '100k' : bot.search(puid=w.puid_col.find()[0]['100k']),
    'snf_hq' : bot.search(puid=w.puid_col.find()[0]['snf_hq']),
    'sherry' : bot.search(puid=w.puid_col.find()[0]['sherry']),
    'dxns' : bot.search(puid=w.puid_col.find()[0]['dxns']),
    'sun_palace' : bot.search(puid=w.puid_col.find()[0]['sun_palace']),
    'change_team' : bot.search(puid=w.puid_col.find()[0]['change_team']),
    }

# init mongo
m = MongoDBPipeline()
profile_col = m.setCol('nosoyyo', 'profile').col

# +++++++++++++++++++++++++
# storing wx group messages
# +++++++++++++++++++++++++

# mao4 pao4
def bubble(type='b'):
    
    # stochastically speak something nonsense from blahlist
    if type == 'b':
        
        try:
            # empty col for now
            blah_col = m.setCol('corpus','wx').col.blah
            blah = random.choice(blah_col.find()[0]['snf'])
            w.staff['snf'][0].send(blah)

            # result
            print('blah-blahed\n[' + blah +']\ninto Strangers & Freaks.')
        except Exception as e:
            print(e)

    # a.k.a 'a fallen night', randomly repeat something that was said by others some time ago.
    elif type == 'r':

        try:
            cl = []
            for i in range(0,m.setCol('corpus','wx.bb5b803d').col.count()):
                cl.append(m.setCol('corpus','wx.bb5b803d').col.find()[i]['content'])
                i += 1
            recurrent = random.choice(cl)
            w.staff['snf'][0].send(recurrent)

            # result
            print('re-send['+recurrent+'] .')
        except Exception as e:
            print(e)

    else:
        print('invalid bubble type')

    return

def main():

    # this script is only for store wx group messages for now
    @bot.register(Group, except_self=False)
    def storeGroupMessages(msg):

        # set storing place, store messages by `the sender`.puid, it's group puid when `the sender` is group.
        wx_col = m.setCol('corpus', 'wx.' + msg.sender.puid).col

        if msg.sender.puid in w.puid_col.find()[0].values():
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
