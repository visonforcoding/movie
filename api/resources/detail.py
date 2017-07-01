# coding=utf-8
from flask_restful import Resource
from model import base
import requests
from common import logger
import json
import logging


class Detail(Resource):

    def get(self, query):
        mongo = base.Mongo.getInstance()
        nosql = {'hash': query}
        fields = {'scrapy_site': 0, 'scrapy_url': 0}
        res = {'ret': 0, 'data': None}
        movie_collection = mongo.mdb.movie
        movie = mongo.mdb.movie.find_one(nosql, fields)
        update_doc = dict()
        if movie:
            if not movie.has_key('db_subject'):
                logger = logging.getLogger("root.file")
                movie_title = movie['title']
                movie_title = movie_title.encode('utf-8')
                logger.info('%s被拿去豆瓣匹配' % movie_title)
                api_url = 'https://api.douban.com/v2/movie/search?q=' + movie_title

                douban_res = requests.get(api_url)
                res_obj = json.loads(douban_res.content)
                if res_obj['total'] > 1 or res_obj['total'] == 1:
                    douban_subject = res_obj['subjects'][0]
                    update_doc = {
                        'db_match': True,
                        'db_subject': douban_subject
                    }
                    movie_collection.update_one({'_id': movie['_id']}, {
                        '$set': update_doc
                    })
                    logger.info('%s匹配成功' % str(movie_title))
                    dict.update(movie,update_doc)
            del movie['_id']
            res['data'] = movie
        else:
            res['ret'] = 1
            res['msg'] = 'not found'
        return res, {'Access-Control-Allow-Origin': '*',
                     'Access-Control-Allow-Methods': 'PUT,GET'}
