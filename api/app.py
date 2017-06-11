from flask import Flask
from flask_restful import Resource, Api
from resources.movie import Movie
# from common import config
from model import base
app = Flask(__name__)
api = Api(app)

base.Mongo.getInstance()

api.add_resource(Movie, '/movie/<string:query>','/')

if __name__ == '__main__':
    app.run(debug=True)