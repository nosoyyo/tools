#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'nosoyyo'

import random
import pymongo
import requests
from bs4 import BeautifulSoup
import json


class Question:

	title = ''
	id = ''
	url = 'http://www.zhihu.com/question' + str(id)
	answer_count = 0


def get_question(url, ):
    question = Pizza()
    pizza.prepare()
    pizza.bake()
    pizza.cut()
    pizza.box()
    return pizza