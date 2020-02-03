import os


class BaseConfig:
    """ Base configuration. """
    SECRET_KEY = os.getenv('AK2_SECRET_KEY', 'SECRET_KEY')
    VIDEO_PATH = os.getenv('AK2_VIDEO_PATH', 'C:\\Users\\serge\\Projects\\ak2-server-videos')
    DATABASE_URI = os.getenv('AK2_DATABASE_URI')
    DATABASE_SCHEMA = os.getenv('AK2_DATABASE_SCHEMA')
    LANGUAGES = ['en', 'ru']


class DevelopmentConfig(BaseConfig):
    """ Development configuration. """
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4


class ProductionConfig(BaseConfig):
    """ Production configuration. """
    BCRYPT_LOG_ROUNDS = 13
    DEBUG = False
