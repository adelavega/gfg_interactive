import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '\xc8U;\xe2w\xb3[c-:\xceeKu\xc9f\xd2\xaac\xfb\x1dZ\xc2\xc2'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    DASHBOARD_PASS = 'cortex24!'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

    try:
        SQLALCHEMY_DATABASE_URI = os.environ['OPENSHIFT_POSTGRESQL_DB_URL']
    except:
        pass


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


