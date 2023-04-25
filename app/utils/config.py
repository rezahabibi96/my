import os
from decouple import config


basedir = os.path.abspath(os.path.dirname(__name__))


class Config():

    CSRF_ENABLED = True
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app\database\database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB = os.path.join(basedir, 'app\database\database.db')
    SQL = os.path.join(basedir, 'app\database\database.sql')
    JSON = os.path.join(basedir, 'app\database\database.json')