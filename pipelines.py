# -*- coding: utf-8 -*-
# flake8: noqa
# @vån
__author__ = 'nosoyyo'

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

# 0.1 basically setup
# 0.2 base class changed into singleton mode; added user/pwd auth;

import pymongo
from wxpy import *

# init
settings = {
            #'MONGODB_SERVER' : 'localhost',
            'MONGODB_SERVER' : '123.207.40.50',
            'MONGODB_PORT' : 27017,

            # password doesn't work this way
            'MONGODB_USERNAME' : 'test',
            #'MONGODB_PASSWORD' : 'testPassword',

            'MONGODB_SSL' : False,
            'MONGODB_SSL_CERTFILE' : '/etc/ssl/client.pem',
            'MONGODB_SSL_KEYFILE' : '/etc/ssl/mongodb.pem',
            'MONGODB_DB' : 'testdb',
            'MONGODB_COL' : 'testcol',

            # Wxpy
            'WxpyDBName' : 'nosoyyo',
            'WxpyUsername' : 'test',
            'WxpyPassword' : 'testPassword',
            'WxpyProfileCol' : 'profile',
            'cache_path' : True,
            'console_qr' : True,
           
            # Qiniu
            'BUCKET_NAME' : 'msfc',
            'QINIU_USERNAME' : 'nosoyyo',
            'QINIU_PROFILE' : 'profile.qiniu',
            'QINIU_PRIVATE' : 'http://p3f2fmqs8.bkt.clouddn.com/',

            # twitter
            'TWITTER_USERNAME' : 'nosoyyo', 
            'TWITTER_PROFILE' : 'profile.twitter',
           }

# ==================
# MongoDB quickstart
# ==================

class Singleton(object):
    _instance = None
    def __new__(cls, dbname, username, password, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)  
        return cls._instance 

class MongoDBPipeline(Singleton):

    def __init__(self, dbname, username, password, settings=settings, ):

        self.client = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT'],
            username=username,
            password=password,
            ssl=settings['MONGODB_SSL'],
            #ssl_certfile=settings['MONGODB_SSL_CERTFILE'],
            #ssl_keyfile=settings['MONGODB_SSL_KEYFILE'],
        )
        self.db = self.client.get_database(dbname)
        self.auth = self.db.authenticate(username, password)
        self.col = self.db.get_collection(settings['MONGODB_COL'])

    def setDB(self, dbname):
        self.db = self.client.get_database(dbname)
        return self

    def setCol(self, dbname, colname):
        self.db = self.client.get_database(dbname)
        self.col = self.db.get_collection(colname)
        return self

    def ls(self):
        return self.db.list_collection_names()


# ===============
# wxpy quickstart
# ===============

class WxpyPipeline():

    def __init__(self, cache_path=True, console_qr=True,):
        self.bot = Bot(settings['cache_path'], settings['console_qr'])
        self.bot.enable_puid()
        return 

    m = MongoDBPipeline(settings['WxpyDBName'], settings['WxpyUsername'], settings['WxpyPassword'])
    puid_col = m.setCol(settings['WxpyDBName'], 'profile').col.wx.puid

    # get staff list


# ================
# Qiniu quickstart
# ================

class QiniuPipeline():

    # import
    from qiniu import Auth, BucketManager, put_file, etag, urlsafe_base64_encode
    import qiniu.config

    def __init__(self, dbname, username, password):
        self.m = MongoDBPipeline(dbname,username,password)
        self.m_auth = self.m.auth
        self.keys = self.m.setCol(settings['QINIU_USERNAME'], settings['QINIU_PROFILE']).col.find()[0]['keys']
        self.access_key = self.keys['access_key']
        self.secret_key = self.keys['secret_key']
    
        # 构建鉴权对象
        self.auth = self.Auth(self.access_key, self.secret_key)
    
        # bucket
        self.bucket = BucketManager(self.auth)

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
        url = self.auth.private_download_url(settings['QINIU_PRIVATE'] + key)
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

    def __init__(self, dbname, username, password):

        # import
        import tweepy

        # init m
        self.m = MongoDBPipeline(dbname, username, password)
        self.m_auth = self.m.auth
        self.keys = self.m.setCol(settings['TWITTER_USERNAME'], settings['TWITTER_PROFILE']).col.find()[0]['keys']

        # get keys
        consumer_key = self.keys['consumer_key']
        consumer_secret = self.keys['consumer_secret']
        access_token = self.keys['access_token']
        access_token_secret = self.keys['access_token_secret']

        # auth and get APIs
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret) 
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(self.auth)
