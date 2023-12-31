import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    username = "root"
    password = "QWEasdzxc123"
    dbname = "krishig_db"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{username}:{password}@192.168.29.22/{dbname}"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'heythisisthesecretkey'

class bucket_name:
    name="krishig"
    region='ap-south-1'

class slider_bucket_name:
    name="krishig-salesuser-slider"
    region='ap-south-1'

