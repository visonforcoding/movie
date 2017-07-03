# coding=utf-8
from flask_restful import Resource
from model import base


class Movie(Resource):

    def get(self, query):
        mongo = base.Mongo.getInstance()
        nosql = {'$or': [
            {'title': {'$regex': '^%s' % query}},
            {'db_subject.title': {'$regex': '^%s' % query}},
        ]}
        fields = {'_id': 0, 'scrapy_site': 0,
                  'scrapy_url': 0, 'create_time': 0,'match_time':0}
        res = {'ret': 0, 'data': None}
        cursor = mongo.mdb.movie.find(nosql, fields).limit(10)
        movies = []
        if cursor:
            for doc in cursor:
                movies.append(doc)
            res['data'] = {'counts': len(movies), 'movies': movies}
        else:
            res['ret'] = 1
            res['msg'] = 'not found'
        return res, {'Access-Control-Allow-Origin': '*',
                     'Access-Control-Allow-Methods': 'PUT,GET'}
