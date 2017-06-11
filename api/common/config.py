class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True
    MDB_URL = 'mongodb://localhost:27017/'
    MDB = 'movie'

class TestingConfig(Config):
    pass