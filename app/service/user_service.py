from app.models import Users,Roles
from sqlalchemy import exc
from app.validation import email_validation
from app import db
def get_users_list(args):
    try:
        if "id" in args.keys() and args["id"] is not None:
            user_data = Users.query.filter_by(id=args["id"]).first()
            return user_data.serialize
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
            return data_list
    except Exception as e:
        print("Error: ",e.__repr__())
        return e.__repr__(), 409

def post_user_details(data):
    try:
        if email_validation(data["email"]) == "Invalid Email":
            return "please enter an email id", 406
        if data != None:
            add_user = Users(
                username=data['username'],
                fullname=data['fullname'],
                email=data['email'],
                mobile_number=data['mobile_number'],
                adhaar_number=data['adhaar_number'],
                password=data['password'],
                House_number=data['House_number'],
                landmark=data['landmark'],
                pincode=data['pincode'],
                city=data['city'],
                state=data['state'],
                Role=int(data['Role'])
            )
            db.session.add(add_user)
            db.session.commit()
            return "Account Created"
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(),409

def patch_users(data,args,public_id):
    try:
        data["modified_by"] = public_id
        user_id=None
        if "id" in args.keys() and args["id"] is not None:
            user_id = args["id"]
        else:
            return "id not passed", 400
        if Users.query.filter_by(id=user_id).first() is not None:
            Users.query.filter_by(id=user_id).update(data)
            db.session.commit()
            return "Data Modified",200
        else:
            return "No Data found",404
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(),409

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
            return "Data Deleted",200
        else:
            return "Data not found", 404
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(), 409