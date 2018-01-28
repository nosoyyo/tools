#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'nosoyyo'

import pymongo


settings = {
            'MONGODB_SERVER' : 'localhost',
            'MONGODB_PORT' : 27017,
            'MONGODB_DB' : 'test',
            'MONGODB_COLLECTION' : 'test',
            }

class MongoDBPipeline():

    def __init__(self, some_setting_list):

        self.client = pymongo.MongoClient(
            some_setting_list['MONGODB_SERVER'],
            some_setting_list['MONGODB_PORT']
        )
        self.db = self.client.get_database(some_setting_list['MONGODB_DB'])
        self.col = self.db.get_collection(some_setting_list['MONGODB_DB'])
