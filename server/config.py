import os
from os.path import abspath, split, dirname
from dotenv import load_dotenv


dotenv_path = split(abspath(__file__))[0].replace('server', '.env')
load_dotenv(dotenv_path)


class Config(object):
    BASE_DIR = dirname(__file__)
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfiguration(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfiguration(Config):
    TESTING = True
    DEBUG = False
    JSONIFY_PRETTYPRINT_REGULAR=False
    SQLALCHEMY_DATABASE_URI = "postgresql://andeladeveloper@localhost:5432/test_mtracker"

app_configuration = {
    'production': Config,
    'development': DevelopmentConfiguration,
    'testing': TestingConfiguration
}
