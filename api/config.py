import os


class BaseConfig:
    """ Base configuration. """
    SECRET_KEY = os.getenv('AK2_SECRET_KEY', 'SECRET_KEY')
    DATABASE_URI = os.getenv('AK2_DATABASE_URI')
    DATABASE_SCHEMA = os.getenv('AK2_DATABASE_SCHEMA')


class DevelopmentConfig(BaseConfig):
    """ Development configuration. """
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4


class ProductionConfig(BaseConfig):
    """ Production configuration. """
    BCRYPT_LOG_ROUNDS = 13
    DEBUG = False
