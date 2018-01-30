#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'nosoyyo'

import time
import random

from quickstart import *
from pretommy import headers, getTheSpan

# init
media_list = ['yoyocelinebellsleeve1', 'pernilleoveralls3', 'pernloewe', 'backvetem', 'veronikaacne-1', 'aliceblomfeldt1', 'emmanuellegeraldineny', 'drakeldn3', 'gioceline1', 'celinetrapezegroup2', 'dakotagucci', 'camillebui', 'ss17-new-york-womens-8-20-of-31', 'dilettabparis6', 'ss17-london-womens-1-of-41', 'ss17-ny-womens-2-16-of-118', 'robertavete', 'leilacamel', 'veravancoach', 'dsc-2400', 'jlorenzoparis', 'guccirings', 'pinstripeceline', 'alexialv2', 'repossigaia4', 'mvacthparis-1', 'ss17-new-york-womens-8-15-of-31', 'alixny', 'celinesmoke1-1', 'natballv', 'cristinaparis1', 'isaacflony1', 'malgosiabelablack', 'frederikkeny', 'ss17-london-womens-10-of-41', 'pernilleldn', 'schaveznyc', 'ss17-milan-womens-62-of-84', 'azimmermilan', 'sylviadries1', 'lululv1', 'henderraf', 'ss17-london-womens-21-of-41', 'mansurgavrielstreet6', 'celinenetysl', 'lauraparis', 'dsc-2902', 'lvflts', 'saskianygivenchy2', 'ediemica', 'sharrisceline1', 'ursinalvgucci', 'gaialv3', 'iselingem', 'ss17-milan-womens-24-of-84', 'diorbuckles', 'celinekhakidets', 'jennybrooches2', 'alexcampernille', 'braschpajamas', 'anagmilan1', 'ss17-ny-womens-2-44-of-118', 'anyared2', 'ss17-new-york-womens-8-25-of-31', 'celinesleeve', 'pernilleceline13', 'alphabombgucci', 'michidelane', 'nicksullivanmilan', 'lamekacoach', 'lchadwick1', 'bellahadidparis', 'celinebags', 'taylorparis', 'celinelace', 'ss17-ny-womens-5-44-of-50', 'giorgiamilan1', 'guccimonogram2', 'masparis1', 'chanelbagssigns', 'natbalenciaga', 'rianneten1', 'yukislip', 'giovannaorange', 'pernillefringe1-copy', 'parismod1', 'acfparis', 'edunmansur', 'miragucciny2-1', 'ttaitvete1', 'jeanldn', 'adaloewe', 'ckaltuzarra', 'dsc-2211', 'celinering', 'mgceline', 'adaparis3-1', 'pernillemilano', 'lexibinxcoach-1', 'ss17-ny-womens-6-34-of-55', 'celinewhitesneakers', 'lilyaldridgeprotagonist', 'ss17-milan-womens-35-of-84', 'nyfloralblouse', 'celinezebrabag1', 'hayettldn1', 'mgrayceline1', 'luisaglv', 'celinesplitsleeve1', 'amaliecoach', 'repossilouisvuitton', 'veronikachloe1', 'celinedetails', 'ayacoach', 'waleskaberet', 'ss17-ny-womens-2-92-of-118', 'cbraschparis', 'crisrose', 'dossldn', 'rvrmicany-1', 'bateslayers', 'teddyshearling', 'vtrainany2', 'guccilogobags', 'aymelinevalentino', 'gildajwdries', 'romeeny', 'pernilleloeweny', 'celineparisorange1', 'emmanuelleparis', 'anyahindmarchnatgold2', 'stellataylor1', 'bagnet', 'lorelleparis1', 'marthahuntny2', 'ss17-new-york-womens-8-28-of-31', 'modelsdries', 'ttaitlthr', 'alessandracodgucci1', 'megangrayparisceline', 'guccisequins1-1', 'pernilleparislv1', 'francescomilan', 'vetementsgucci', 'cgdetails', 'ssampaiony', 'aspencersydney', 'hedcamtrioparis4', 'graceelizabeth', 'lvmas1', 'giacoppolagucci1', 'sharrisldn-1', 'jennymilan', 'vhalessandrarich1', 'hermestotebag', 'mansurgavrielstreet7', 'ss17-new-york-womens-7-57-of-72', 'ss17-london-womens-18-of-41', 'gildanyc', 'gildagiorgia', 'dsc-2236', 'takahirotokyo', 'irinacel', 'jwcufflv1', 'mirandakerrlv', 'gildatuileries2', 'ss17-new-york-womens-7-23-of-72', 'yasmingucci', 'ss17-ny-womens-2-48-of-118', 'anamilano1', 'ruthbellldn', 'lvtrioparis1', 'pernpleats', 'aymelineproenza', 'veronikaheillv2', 'ss17-ny-womens-2-65-of-118', 'ss17-london-womens-2-of-41', 'hgdior1', 'teddyhari', 'guccimonogrambag2-1', 'nywidebrim', 'nhartleyny', 'dakotakaren1', 'gildavetements1', 'loewenyc', 'ss17-london-womens-22-of-41', 'ss17-ny-womens-5-15-of-50', 'camnyc1', 'loeweaymeline', 'maartjeverhoefcoach', 'girlsmilano', 'bomberjktldn', 'miyakeceline', 'mansurgavrielstreet1', 'mansurgavrielstreet5', 'langleyfoxny', 'jennymilan-1', 'celineldn5', 'josephineskrivervs', 'ss17-ny-womens-6-15-of-55', 'pradavirgil', 'ss17-london-womens-41-of-41', 'veronikamilan1', 'alixnyc', 'adidasval', 'waleskagorczevskiparis2', 'ss17-new-york-womens-7-14-of-72', 'aspencerny', 'chloelvldn', 'arimilan', 'hgslip1', 'loewewindblown', 'lottaparis', 'celineluggageflat', 'sharrisgucci1', 'anninaallwhite4', 'guccifloralmono', 'crocheels', 'celineshrt', 'phoebeceline-1', 'pernillevetements', 'lchadwickny', 'lvcelinecoffee', 'anninamislinnyc3', 'lauralovegucci5', 'guccigrograin', 'crisherrman', 'adaparis1', 'maenyc', 'cbraschnielsonchanel3', 'fmlecel', 'megpattyny', 'celineearring', 'jennyny', 'juliahafstromparis', 'gaiarepossiphone', 'loliparis1', 'gaialoewesuede', 'karenelsongucci2', 'sophiebuhaiparis4', 'ildaracuin-asldn', 'lvmono', 'dsc-2614', 'sharrisldn-2', 'gildilet1', 'rippedgucciflats', 'leafceline1', 'hgotildaxiaofree', 'mdlcurlsldn', 'cherrmann1', 'lvtrio', 'gildapradany', 'camcha', 'dsc-2750', 'eweiss1', 'vetementsldn', 'gucciclogs', 'lvjane1', 'anjachloeparis9', 'dvnparis', 'anninamaiyet', 'candelaada', 'dilettalv']

mongodb_init = {
            'MONGODB_SERVER' : 'localhost',
            'MONGODB_PORT' : 27017,
            'MONGODB_DB' : 'fashion',
            'MONGODB_COLLECTION' : 'tommy',
            }

m = MongoDBPipeline(mongodb_init)
m.switch('fashion', 'tommy')

# init ml
ml = media_list

# init h&c
headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
headers['Referer'] = 'http://www.tommyton.com/'

cookies = {}
cookies['_ga'] = 'GA1.2.818511824.1517175768'
cookies['_gid'] = 'GA1.2.756456048.1517175768'

# main
for i in range(0, len(media_list)):
	
	# check if exists
	if len(m.col.find({'Media':'yoyocelinebellsleeve1'})[0].keys()) <= 2:
		
		# bao1 tang1 luo1
		xhr = 'http://www.tommyton.com/media/' + ml[i]
		headers['Host'] = 'http://www.tommyton.com'
		soup = cookXHRSoup(xhr, headers=headers, cookies=cookies)