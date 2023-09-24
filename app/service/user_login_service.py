import jwt
from functools import wraps
from datetime import datetime,timedelta
from app.config import *
from app.models import Users
from app import request
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='app.log',
                    filemode='a')
def post_user_login(auth):
    user = None
    if not auth or not auth["username"] or not auth["password"]:
        return "could not verify"
    user = Users.query.filter_by(username=auth["username"], password=auth["password"]).first()
    if user is not None:
        if user.password:
            token = jwt.encode({
                'public_id': user.id,
                'username': user.username,
                'role': user.Role,
                'exp': datetime.utcnow() + timedelta(days=7)
            }
                , BaseConfig.SECRET_KEY,
                "HS256"
            )
            response = {
                "error": False,
                "message": "Token Generated",
                "data":{
                    "token": token
                }
            }
            return response,201
    response = {
        "error": True,
        "message": "login failed",
        "data": None
    }
    return response, 401

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers["Authorization"]
        if not token:
            response={
                "error": True,
                'message': 'token is missing',
                "data": None
            }
            return response, 401
        try:
            data = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms='HS256')
            current_user = Users.query.filter_by(id=data['public_id']).first()

        # print(current_user.user_role)
        except Exception as e:
            print(e)
            logging.error("200"+"-"+e.__repr__())
            response = {
                "error": True,
                'message': 'Please login again!',
                "data": None
            }
            return response, 200
        return f(current_user, *args, **kwargs)
    return decorated
