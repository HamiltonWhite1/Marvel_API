import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    FLASK_APP= os.getenv('FLASK_APP')
    FLASK_ENV= os.getenv('FLASK_ENV')
    SECRET_KEY= os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace('postgres', 'postgresql')
    SQLALCHEMY_TRACK_MODIFICATIONS = False