from common import config
from pymongo import MongoClient
class Mongo():
    __instance = None

    def __init__(self):
        app_config = config.DevelopmentConfig()
        mdb_url = app_config.MDB_URL
        self.mdb_client = MongoClient(mdb_url)
        self.mdb = self.mdb_client[app_config.MDB]
        print 'mongo init....'

    @staticmethod
    def getInstance():
        if Mongo.__instance is None:
            Mongo.__instance = Mongo()
        return Mongo.__instance