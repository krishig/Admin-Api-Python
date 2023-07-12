from app.models import Users,Roles
from sqlalchemy import exc
from app.validation import email_validation
from app import db
def get_users_list(args):
    try:
        if "id" in args.keys() and args["id"] is not None:
            user_data = Users.query.filter_by(id=args["id"]).first()
            response={
                "error": False,
                "message": "details of user",
                "data":user_data.serialize
            }
            return response
        else:
            user_data = Users.query.all()
            data_list = []
            for i in user_data:
                # data = {}
                # data["id"] = i.id
                # data["username"] = i.username
                # data["fullname"] = i.fullname
                # data["email"] = i.email
                # data["mobile_number"] = i.mobile_number
                # data["adhaar_number"] = i.adhaar_number
                # data["password"] = i.password
                # data["city"] = i.city
                # data["state"] = i.state
                # data["Role"] = i.Role
                # data["created_at"] = str(i.created_at)
                # data["modified_at"] = str(i.modified_at)
                data={}
                data_list.append(i.serialize)
            response={
                "error": False,
                "message": "list of users",
                "data": data_list
            }
            return response
    except Exception as e:
        print("Error: ",e.__repr__())
        response={
            "error": True,
            "message": e.__repr__(),
            "data": None
        }
        return response, 409

def post_user_details(data):
    try:
        if email_validation(data["email"]) == "Invalid Email":
            return "please enter an email id", 406
        if data != None:
            add_user = Users(
                username=data['username'],
                fullname=data['fullname'],
                email=data['email'],
                gender=data['gender'],
                mobile_number=data['mobile_number'],
                aadhaar_number=data['aadhaar_number'],
                password=data['password'],
                house_number=data['house_number'],
                landmark=data['landmark'],
                pincode=data['pincode'],
                district=data['district'],
                city=data['city'],
                state=data['state'],
                Role=int(data['Role'])
            )
            db.session.add(add_user)
            db.session.commit()
            user_data = Users.query.filter_by(username=data['fullname']).first()
            response={
                "error": False,
                "message": "account created",
                data: user_data.serialize
            }
            return response
    except Exception as e:
        print("Error: ", e.__repr__())
        response = {
            "error": True,
            "error_msg": e.__repr__(),
            "message": "something went wrong",
            "data": None
        }
        return response,409

def patch_users(data,args,public_id):
    try:
        data["modified_by"] = public_id
        user_id=None
        if "id" in args.keys() and args["id"] is not None:
            user_id = args["id"]
        else:
            response ={
                "error": True,
                "message": "id not passed",
                "data": None
            }
            return response, 400
        if Users.query.filter_by(id=user_id).first() is not None:
            Users.query.filter_by(id=user_id).update(data)
            db.session.commit()
            user_data = Users.query.filter_by(id=user_id).first()
            response={
                "error": False,
                "message": "data modified",
                "data": user_data.serialize
            }
            return response,200
        else:
            response={
                "error": True,
                "message": "no data found",
                "data": None
            }
            return response,404
    except Exception as e:
        print("Error: ", e.__repr__())
        response = {
            "error": True,
            "message": e.__repr__(),
            "data": None
        }
        return response,409

def delete_users(args):
    try:
        user_id = None
        if "id" in args.keys() and args["id"] is not None:
            user_id = args["id"]
        else:
            return "id not passed", 400
        data = Users.query.filter_by(id=user_id).first()
        if data is not None:
            db.session.delete(data)
            db.session.commit()
            user_data = Users.query.all()
            response={
                "error": False,
                "message": "data deleted",
                "data": [i.serialize for i in user_data]
            }
            return response,200
        else:
            response = {
                "error": False,
                "message": "data not found",
                "data": None
            }
            return response, 404
    except Exception as e:
        print("Error: ", e.__repr__())
        response={
            "error": True,
            "message": e.__repr__(),
            "data": None
        }
        return response, 409