# -*- coding: utf-8 -*-
# flake8: noqa


# usage
# 
# from web to qiniu:
# q = QiniuPipeline()
# pic_url = 'http://some.pic.url'
# ret = q.upload(pic_url)
# 
# from qiniu to distribution:
# q = QiniuPipeline()
# downloadable_file_url = q.getFile(key)

import pymongo

from wxpy import *
from qiniu import Auth, BucketManager, put_file, etag, urlsafe_base64_encode
import qiniu.config


# ==================
# Pipeline Base Class
# ==================

# init
settings = {
            # MongoDB
            'MONGODB_SERVER' : 'localhost',
            'MONGODB_PORT' : 27017,
            'MONGODB_DB' : 'testdb',
            'MONGODB_COLLECTION' : 'testcol',

            # Wxpy
            'WxpyUser' : 'nosoyyo',
            'WxpyProfileCol' : 'profile',
           
            # Qiniu
            'BUCKET_NAME' : 'msfc',
            'QINIU_USERNAME' : 'nosoyyo',
            'QINIU_PROFILE' : 'profile.qiniu',
           }

# ==================
# MongoDB quickstart
# ==================

# v0.1
class MongoDBPipeline():

    def __init__(self, settings=settings):

        self.client = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = self.client.get_database(settings['MONGODB_DB'])
        self.col = self.db.get_collection(settings['MONGODB_COLLECTION'])

    def setDB(self, db):
        self.db = self.client.get_database(db)
        return self

    def setCol(self, db, col):
        self.db = self.client.get_database(db)
        self.col = self.db.get_collection(col)
        return self

# ===============
# wxpy quickstart
# ===============

class WxpyPipeline():

    m = MongoDBPipeline()
    puid_col = m.setCol('nosoyyo', 'profile').col.wx.puid

    # init bot
    bot = Bot(cache_path=True, console_qr=True)
    bot.enable_puid()

    staff = {
        'myself' : bot.self,
        'msfc' : bot.search(puid=puid_col.find()[0]['msfc']),
        'snf' : bot.search(puid=puid_col.find()[0]['snf']),
        '100k' : bot.search(puid=puid_col.find()[0]['100k']),
        'snf_hq' : bot.search(puid=puid_col.find()[0]['snf_hq']),
        'sherry' : bot.search(puid=puid_col.find()[0]['sherry']),
        'dxns' : bot.search(puid=puid_col.find()[0]['dxns']),
        'sun_palace' : bot.search(puid=puid_col.find()[0]['sun_palace']),
        'change_team' : bot.search(puid=puid_col.find()[0]['change_team']),
        }

# ================
# Qiniu quickstart
# ================

class QiniuPipeline():

    m = MongoDBPipeline()
    keys = m.setCol(settings['QINIU_USERNAME'], settings['QINIU_PROFILE']).col.find()[0]['keys']
    access_key = keys['access_key']
    secret_key = keys['secret_key']
    # 构建鉴权对象
    auth = Auth(access_key, secret_key)
    
    # bucket
    bucket = BucketManager(auth)

    #要上传的空间
    bucket_name = settings['BUCKET_NAME']

    #上传到七牛后保存的文件名前缀
    #prefix = 'tommy'

    def upload(self, pic_url):
        bucket_name = self.bucket_name
        key = pic_url.split('/')[-1]
        token = self.auth.upload_token(bucket_name, key, 0)
        ret = self.bucket.fetch(pic_url, bucket_name, key)
        return ret

    def getFile(self, key):
        url = self.auth.private_download_url('http://p3f2fmqs8.bkt.clouddn.com/' + key)
        return url

    def ls(self):
        l = self.bucket.list(self.bucket_name)[0]['items']
        return l

    def count(self):
        c = len(self.bucket.list(self.bucket_name)[0]['items'])
        return c
