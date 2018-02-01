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
m.switch('nosoyyo', 'profile')

# +++++++++++++++++++++++++
# storing wx group messages
# +++++++++++++++++++++++++

# init bot
bot = Bot(cache_path=True, console_qr=True)
bot.enable_puid()

# init selected groups_puid
groups_puid = {
        'myself' : m.col.wx.find()[0]['groups']['myself']
        'msfc' : m.col.wx.find()[0]['groups']['msfc']
        'snf' : m.col.wx.find()[0]['groups']['snf']
        '100k' : m.col.wx.find()[0]['groups']['100k']
        'snf_hq' : m.col.wx.find()[0]['groups']['snf_hq']
        'sherry' : m.col.wx.find()[0]['groups']['sherry']
        'dxns' : m.col.wx.find()[0]['groups']['dxns']
        'sun_palace' : m.col.wx.find()[0]['groups']['sun_palace']
        'change_team' : m.col.wx.find()[0]['groups']['change_team']
        }

# here is the only place you need to turn on/off, hopefully
switch = [

# personal
            'myself'
#           'msfc',
            'snf',
            'snf_hq',
            'sherry',

# zhihu
            '100k',
            'dxns',
            'sun_palace',
            'change_team',
# football
            ]

# debugging construct payload_list
# plan to get payload resource from some APIs
payload_list = []

# Delivery class
class Delivery():
    dest = ''
    payload = ''
#   isPayloadSent = False

    def loadUp(self, payload):
        self.payload = str(payload)
#       isPayloadSent = False
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
#       self.isPayloadSent = True
#       self.unLoad()
        return print('Successfully sent 1 payload.')

# construct queue
def queue():
    queue= {}
    for i in range(0, len(switch)):
        queue[switch[i]] = Delivery()
        queue[switch[i]].dest = groups_puid[switch[i]]
    return queue

def scheduledTask():
    queue = queue()
    while True:
        if '7' in str(datetime.datetime.now().minute):
            for key in queue:
#               if not queue[key].isPayloadSent:
                queue[key].deliver(queue[key].dest)
                boringWait(100)

def main():

    # this script is only for store wx group messages for now
    @bot.register(Group, except_self=False)
    def storeGroupMessages(msg):

        if msg.sender.puid in list(groups_puid.values()):
            if msg.type == 'Text':
                m.col.insert({
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
                m.col.insert({
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
                m.col.insert({
                    'group' : msg.sender.name,
                    'message_id' : msg.id,
                    'message_type' : msg.type,
                    'content' : msg.url,
                    'create_time' : msg.create_time.ctime(),
                    'sender' : msg.member.name,
                    'sender_puid' : msg.member.puid,
                    })
            elif msg.type == 'Video':
                m.col.insert({
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
                m.col.insert({
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
                m.col.insert({
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
                m.col.insert({
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
