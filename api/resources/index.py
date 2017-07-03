# coding=utf-8
from flask_restful import Resource
from model import base
from datetime import datetime


class Index(Resource):

    def get(self):
        res = {'ret': 0, 'data': None}        
        newMovies = self.getNewMovies();
        ratingMovies = self.getRatingMovies();
        res['data'] = {'new_movies': newMovies,'rating_movies':ratingMovies}
        return res, {'Access-Control-Allow-Origin': '*',
                     'Access-Control-Allow-Methods': 'PUT,GET'}

    def getNewMovies(self):
        mongo = base.Mongo.getInstance()
        nosql = {}
        fields = {'_id': 0, 'scrapy_site': 0,
                  'scrapy_url': 0}
        cursor = mongo.mdb.movie.find(
            nosql, fields).sort([('create_time', -1)]).limit(10)
        movies = []
        if cursor:
            for doc in cursor:
                doc['create_time'] = doc['create_time'].strftime(
                    '%Y-%m-%d %H:%M:%S')
                movies.append(doc)
        return movies

    def getRatingMovies(self):
        '''
        获取最新高分电影
        '''
        mongo = base.Mongo.getInstance()
        nosql = {'db_match':True}
        fields = {'_id': 0, 'scrapy_site': 0,
                  'scrapy_url': 0}
        cursor = mongo.mdb.movie.find(
            nosql, fields).sort([('db_subject.rating.average',-1),('create_time', -1)]).limit(5)
        movies = []
        if cursor:
            for doc in cursor:
                doc['create_time'] = doc['create_time'].strftime(
                    '%Y-%m-%d %H:%M:%S')
                movies.append(doc)
        return movies
