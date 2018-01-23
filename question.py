#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import pymongo
import requests
from bs4 import BeautifulSoup
import json

# dirty hacking this codec issue
import locale
locale.setlocale(locale.LC_ALL, 'zh_CN.utf8')

# init session
session = requests.session()

# init pymongo
client = pymongo.MongoClient("localhost", 27017)
db = client.zhihu
col = db["questions"]

# init question_list
question_list = []


# user-agent pool
# debugging | user_agent_list = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36 "]
user_agent_list = [\
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36 "
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "  
    "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",  
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "  
    "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",  
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "  
    "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",  
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "  
    "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",  
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "  
    "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",  
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "  
    "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",  
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "  
    "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",  
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "  
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "  
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",  
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",  
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "  
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
    "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",  
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "  
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",  
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "  
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"  
   ]

# elegant headers
headers = {}
headers['accept'] = 'application/json'
headers['Accept-Encoding'] = 'gzip'
headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,es;q=0.6,it;q=0.5'
headers['authorization'] = 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
headers['Connection'] = 'keep-alive'
headers['Host'] = 'www.zhihu.com'
headers['If-None-Match'] = '"162518edd010e7757f54ee25d925a1e925d5ec9d"'
headers['Referer'] = 'https://www.zhihu.com/topic/19551052/unanswered'
headers['User-Agent'] = random.choice(user_agent_list)
headers['X-UDID'] = 'AGBAMWpRJQqPTsptASgteUMz6KiQODy5QtU='

cookies = {}

# elegant cookies
cookies['xsrf'] = 'ac2d67006e105b97795dc38a4e5cee48'
cookies['d_c0'] = 'AGBAMWpRJQqPTsptASgteUMz6KiQODy5QtU=|1467083062'
cookies['_za'] = 'f16ba396-464e-4285-96c8-711c70be70be'
cookies['_zap'] = 'faa6e47b-d1f2-45ae-a7ed-67263a711d56'
cookies['_ga'] = 'GA1.2.1855889940.1469028543'
cookies['aliyungf_tc'] = 'AQAAAHjs/XoVEQYAJSmIdY9aG1krr99h'
cookies['acw_tc'] = 'AQAAAMFByC1cQwIAbCEV0i0LTkWrtF7K'
cookies['s-t'] = 'autocomplete'
cookies['q_c1'] = '179708b2700b42259e4729e8bb6f0a7d|1515644593000|1467083055000'
cookies['s-q'] = '%E7%8E%8B%E5%A8%81'
cookies['sid'] = '6jr7fkg8'
cookies['s-i'] = '6' 
cookies['__utmc'] = '155987696'
cookies['__utmz'] = '155987696.1516286487.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
cookies['capsion_ticket'] = '2|1:0|10:1516351412|14:capsion_ticket|44:ZDg0YjBhMGI0ZWUyNDVmNGI3MWMzZWU5ZTExZDBmZTA=|ca1d87fe54be7a00b908b3c043ee554541f4b0eae881a87bcafab77941dfc980'
cookies['__utma'] = '155987696.1855889940.1469028543.1516295168.1516351762.3'
cookies['__utmb'] = '155987696.0.10.1516351762'
cookies['r_cap_id'] = 'MTkyYzQ4NGIxMGU0NDE2MThjMmEyMmI0ZTE0NWFhODI=|1516351765|5c9d358625f491cf87e1e9f21121cd90b7e10e5e'
cookies['cap_id'] = 'MzMyYzI2MjNhYTI5NGY4MmJhMTYxMzQwNjBiNmQzNTQ=|1516351765|f4d73377db7ebc56c5799984fb46cd65067bf7cc'
cookies['l_cap_id'] = 'NzIzNGY1MjEyMjM2NDY2ZGJkN2Y1NGY0Y2M4OGJjM2M=|1516351765|135159ca38dc378334611fe3c82de9bac4f1a555'

# turn dict into cookiejar with Cookie_utility
cookies = requests.utils.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)

# define Question
class Question:

    title = ''
    id = ''
    url = 'http://www.zhihu.com/question' + str(id)
    answer_count = 0
    score = 0

    def __str__(self):
        return self.title

    def get_question(url):
        question = Question()
        response = requests.get(url, headers = headers, cookies = cookies)
        soup = BeautifulSoup(response.text, "html.parser")
        res_json = json.loads(response.text)

        question.title = res_json['data'][i]['target']['title']
        question.id = res_json['data'][i]['target']['id']
        question.answer_count = res_json['data'][i]['target']['answer_count']

        return question

    def score_question(question):
        score = 0
        # some scoring operations
        return score


def get_url():
    return url


if __name__ == '__main__':
    




    # debug
    starting_url = 'https://www.zhihu.com/api/v4/topics/19551052/feeds/top_question?include=data%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Darticle)%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Dpeople)%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Danswer)%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Danswer)%5D.target.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Darticle)%5D.target.content%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dquestion)%5D.target.comment_count&limit=20'
# so we're gonna build a url pool maybe later

'''# debug 
for i in range(0, len(res_json['data'])):
    print('')
    print('')
    print('')
    print('http://www.zhihu.com/question/' +str(res_json['data'][i]['target']['id']))
    print(res_json['data'][i]['target']['title'])
    print('已经有 ' + str(res_json['data'][i]['target']['answer_count']) + ' 个回答, ' + str(res_json['data'][i]['target']['follower_count']) + ' 人关注')
    print('以上第 ' + str(i + 1) + ' 个问题')
    print('')
    print('')
    i += 1 
'''

