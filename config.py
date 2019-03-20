import os


class Config:
    DEBUG = True

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

    # ***** ROUTES PREFIX ******
    APPLICATION_ROOT = '/api'

    # ********** DATABASE ***********************
    DATABASE_PATH = 'kpmg-db.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///kpmg-db.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ********** TESTING ************************
    TESTING = False
    # Used in testing. When this is true and client submits a solutions,

    # ********** JWT ****************************
    SECRET_KEY = r'\::b)yV-."#!Fink-6SD-9(dE>O+-S8I,):6}@kfUw;0v\h:4EZU0;1cOv)zag&'


class LocalConfig(Config):
    """ Umbrella config for all local runs, vagrant runs and unit testing runs """
    pass


class ProductionConfig(Config):
    """ Config used in production environment """
    DEBUG = False


class TestConfig(Config):
    DATABASE_PATH = 'test-kpmg-db.db'
    TESTING = True


config = {
    'local': LocalConfig,
    'production': ProductionConfig,
    'test': TestConfig
}

SELECTED_CONFIG = os.getenv('API_ENV', 'local')
