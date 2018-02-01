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

from wxpy import *
from qiniu import Auth, BucketManager, put_file, etag, urlsafe_base64_encode
import qiniu.config


class QiniuPipeline(object):

	access_key = 'Es18UwJ1SNlvINU4Q-k4ci63o9hi3EV_38wqmfvt'
	secret_key = 'qALrsyp5d7EJZ5iezPc_dZUxup_APzWfFZfrUcVK'

	#要上传的空间
	bucket_name = 'msfc'

	#构建鉴权对象
	auth = Auth(access_key, secret_key)

	# bucket
	bucket = BucketManager(auth)

	#上传到七牛后保存的文件名
	prefix = 'tommy'

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


	#生成上传 Token，可以指定过期时间等
	#token = q.upload_token(bucket_name, key, 3600)

'''
#要上传文件的本地路径
localfile = './sync/bbb.jpg'
ret, info = put_file(token, key, localfile)

print(info)
assert ret['key'] == key
assert ret['hash'] == etag(localfile)
'''


# ===============
# wxpy quickstart
# ===============

class WxpyPipeline():

    # init bot
    bot = Bot(cache_path=True, console_qr=True)
    bot.enable_puid()

    staff = {
        'myself' : bot.self,
        'msfc' : bot.groups().search('MSFC')[0],
        'snf' : bot.groups().search('陌生')[0],
        '100k' : bot.groups().search('十万粉')[0],
        'snf_hq' : bot.groups().search('陌怪')[0],
        'sherry' : bot.groups().search('祝雪梨成功')[0],
        'dxns' : bot.groups().search('倒行逆施')[0],
        'sun_palace' : bot.groups().search('太阳宫')[0],
        'change_team' : bot.groups().search('换个新球队')[0],
        }

# ==================
# MongoDB quickstart
# ==================

# Initiate MongoDB
mongodb_init = {
            'MONGODB_SERVER' : 'localhost',
            'MONGODB_PORT' : 27017,
            'MONGODB_DB' : 'testdb',
            'MONGODB_COLLECTION' : 'testcol',
            }

class MongoDBPipeline():

    def __init__(self, settings=mongodb_init):

        self.client = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = self.client.get_database(settings['MONGODB_DB'])
        self.col = self.db.get_collection(settings['MONGODB_COLLECTION'])

    def switch(self, db, col):
        self.db = self.client.get_database(db)
        self.col = self.db.get_collection(col)
        return self

