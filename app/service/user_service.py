import traceback
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from app.models import Users,Roles
from sqlalchemy import exc
from app.validation import email_validation
from app import db
def get_users_list(args,page_no,items_per_page):
    try:
        if "id" in args.keys() and args["id"] is not None:
            user_data = Users.query.filter_by(id=args["id"]).first()
            if user_data is not None:
                response={
                    "error": False,
                    "message": "details of user",
                    "data":user_data.serializer
                }
                return response,200
            else:
                response = {
                    "error": True,
                    "message": "no data found",
                    "data": None
                }
                return response, 404
        else:
            paginate_result = {}
            user_data = Users.query.order_by(text("id desc")).paginate(page=page_no,per_page=items_per_page)
            paginate_result["total_pages"]=user_data.pages
            if user_data.has_next==True:
                paginate_result["next_page"]="/product?items_per_page=%s&page_number=%s"%(items_per_page,page_no+1)
            if user_data.has_prev==True:
                paginate_result["prev_page"] = "/product?items_per_page=%s&page_number=%s" % (items_per_page, page_no - 1)
            if user_data.pages is not None:
                paginate_result["total_pages"]=user_data.pages
            paginate_result["result"]=[x.serializer for x in user_data]
            #data_list = []
            #for i in user_data:
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
                #data={}
                #data_list.append(i.serializer)
            response={
                "error": False,
                "message": "list of users",
                "data": paginate_result
            }
            return response,200
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        error = error[1:len(error)-1].split(",")[1]
        response = {
            "error": True,
            "message": error[2:len(error)-2],
            "data": None
        }
        return response, 409
    except Exception as e:
        print("Error: ",e.__repr__())
        response={
            "error": True,
            "message": "something went wrong",
            "data": None
        }
        return response, 409

def post_user_details(data):
    try:
        if email_validation(data["email"]) == "Invalid Email":
            response = {
                "error": True,
                "message": "Invalid Email",
                "data": None
            }
            return response, 409
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
            user_data = Users.query.filter_by(username=data['username']).first()
            response={
                "error": False,
                "message": "account created",
                "data": user_data.serializer
            }
            return response,200
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        error = error[1:len(error)-1].split(",")[1]
        response = {
            "error": True,
            "message": error[2:len(error)-2],
            "data": None
        }
        return response, 409
    except Exception as e:
        print("Error: ",e.__repr__())
        response = {
            "error": True,
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
                "data": user_data.serializer
            }
            return response,200
        else:
            response={
                "error": True,
                "message": "no data found",
                "data": None
            }
            return response,404
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        error = error[1:len(error)-1].split(",")[1]
        response = {
            "error": True,
            "message": error[2:len(error)-2],
            "data": None
        }
        return response, 409
    except Exception as e:
        print("Error: ", e.__repr__())
        response = {
            "error": True,
            "message": "something went wrong",
            "data": None
        }
        return response,409

def delete_users(args):
    try:
        user_id = None
        if "id" in args.keys() and args["id"] is not None:
            user_id = args["id"]
        else:
            response = {
                "error": True,
                "message": "id not passed",
                "data": None
            }
            return response, 400
        data = Users.query.filter_by(id=user_id).first()
        if data is not None:
            db.session.delete(data)
            db.session.commit()
            user_data = Users.query.all()
            response={
                "error": False,
                "message": "data deleted",
                "data": [i.serializer for i in user_data]
            }
            return response,200
        else:
            response = {
                "error": True,
                "message": "data not found",
                "data": None
            }
            return response, 404
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        error = error[1:len(error)-1].split(",")[1]
        response = {
            "error": True,
            "message": error[2:len(error)-2],
            "data": None
        }
        return response, 409
    except Exception as e:
        print("Error: ", e.__repr__())
        response={
            "error": True,
            "message": "something went wrong",
            "data": None
        }
        return response, 409
