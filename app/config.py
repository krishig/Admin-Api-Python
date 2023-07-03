import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    username = "root"
    password = "QWEasdzxc123"
    dbname = "krishig_db"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{username}:{password}@65.0.252.8:3307/{dbname}"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'heythisisthesecretkey'

class bucket_name:
    name="krishig"
    region='ap-south-1'

