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
# from qiniu import Auth, BucketManager, put_file, etag, urlsafe_base64_encode
# import qiniu.config


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
            'cache_path' : True,
            'console_qr' : True,
           
            # Qiniu
            'BUCKET_NAME' : 'msfc',
            'QINIU_USERNAME' : 'nosoyyo',
            'QINIU_PROFILE' : 'profile.qiniu',

            # twitter
            'TWITTER_USERNAME' : 'nosoyyo', 
            'TWITTER_PROFILE' : 'profile.twitter',
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

    def ls(self):
        return self.db.list_collection_names()


# ===============
# wxpy quickstart
# ===============

class WxpyPipeline():

    def __init__(self,settings=settings, cache_path=True, console_qr=True,):
        self.bot = Bot(settings['cache_path'], settings['console_qr'])
        self.bot.enable_puid()
        return 

    m = MongoDBPipeline()
    puid_col = m.setCol('nosoyyo', 'profile').col.wx.puid

    # get staff list


# ================
# Qiniu quickstart
# ================

class QiniuPipeline():

    # import
    from qiniu import Auth, BucketManager, put_file, etag, urlsafe_base64_encode
    import qiniu.config

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

# ==================
# Twitter quickstart
# ==================

class TwitterPipeline():
    
    # import
    import tweepy

    # init m
    m = MongoDBPipeline()
    keys = m.setCol(settings['TWITTER_USERNAME'], settings['TWITTER_PROFILE']).col.find()[0]['keys']

    # get keys
    consumer_key = keys['consumer_key']
    consumer_secret = keys['consumer_secret']
    access_token = keys['access_token']
    access_token_secret = keys['access_token_secret']

    # auth and get APIs
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)