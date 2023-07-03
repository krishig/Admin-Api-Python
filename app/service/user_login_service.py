import jwt
from functools import wraps
from datetime import datetime,timedelta
from app.config import *
from app.models import Users
from app import request
def post_user_login(auth):
    if not auth or not auth["username"] or not auth["password"]:
        return "could not verify"
    user = Users.query.filter_by(username=auth["username"], password=auth["password"]).first()
    if user.password:
        token = jwt.encode({
            'public_id': user.id,
            'username': user.username,
            'role': user.Role,
            'exp': datetime.utcnow() + timedelta(minutes=45)
        }
            , BaseConfig.SECRET_KEY,
            "HS256"
        )
        return token,201
    return "Login failed", 401

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers["Authorization"]
        if not token:
            return {'Message': ' Token is missing'}, 401
        try:
            data = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms='HS256')
            current_user = Users.query.filter_by(id=data['public_id']).first()

        # print(current_user.user_role)
        except Exception as e:
            print(e)
            return {'Message': 'Token is invalid here'}, 401
        return f(current_user, *args, **kwargs)
    return decorated