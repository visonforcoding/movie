from flask import Flask
from flask_restful import Resource, Api
from resources.movie import Movie
from resources.detail import Detail
from resources.index import Index

# from common import config
from model import base
app = Flask(__name__)
api = Api(app)

base.Mongo.getInstance()

api.add_resource(Movie, '/movie/<string:query>','/')
api.add_resource(Detail, '/detail/<string:query>','/')
api.add_resource(Index, '/index','/')

if __name__ == '__main__':
    app.run(debug=True)