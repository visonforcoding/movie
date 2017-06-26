# coding=utf-8
import requests
# from bs4 import BeautifulSoup
from os import path
from pymongo import MongoClient
import sys
sys.path.append(path.abspath('../'))
import random
import logging
from common import logger
import json


args = sys.argv
try:
    env = args[1]
except:
    env = 'default'

config = {
    'default': {'mdb_host': '127.0.0.1', 'mdb_port': 27017, 'mdb_name': 'movie'},
    'vison': {'mdb_host': '192.168.33.10', 'mdb_port': 27017, 'mdb_name': 'movie'},
}
# mongo

mongoconn = MongoClient(config[env]['mdb_host'], config[env]['mdb_port'])
movie_collection = mongoconn.movie.movie

# create logger
logger = logging.getLogger("root.file")

total_counts = movie_collection.find().count()

random_int = random.randint(0, total_counts - 1)

random_doc = movie_collection.find().limit(1).skip(random_int).next()
movie_title = random_doc['title']
movie_title = movie_title.encode('utf-8')
logger.info('%s被拿去豆瓣匹配' % movie_title)
api_url = 'https://api.douban.com/v2/movie/search?q=' + movie_title

res = requests.get(api_url)
res_obj = json.loads(res.content)
if res_obj['total'] > 1 or res_obj['total'] == 1:
    douban_subject = res_obj['subjects'][0]
    update_doc = {
        'db_match': True,
        'db_subject': douban_subject
    }
    movie_collection.update_one({'_id': random_doc['_id']}, {
        '$set': update_doc
    })
    logger.info('%s匹配成功' % str(movie_title))
elif res_obj['total'] == 0:
    logger.info('%s匹配失败' % str(movie_title))

else:
    logger.info('%s记录过多，跳过更新' % str(movie_title))
