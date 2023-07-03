from flask import Flask,Blueprint,request,jsonify
from flask_restx import Api,Resource,fields,Namespace,reqparse
from .config import BaseConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
#from flask_sqlalchemy.types import BigInteger
app = Flask(__name__)
blueprint=Blueprint('Api',__name__,url_prefix="/python")
CORS(app)
api = Api(blueprint,doc='/',default_label="Orders",title="Admin Api")
app.config['SWAGGER_UI_JSONEDITOR']=True
app.config.from_object(BaseConfig)
app.config['MAX_CONTENT_LENGTH'] = 1024*1024*3
db = SQLAlchemy(app)
app.register_blueprint(blueprint)
migrate = Migrate(app, db,compare_type=True)

from . import routes,models