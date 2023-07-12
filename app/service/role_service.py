from app.models import Roles
from app import db
from sqlalchemy.exc import SQLAlchemyError
def get_role_list():
    try:
        data_list = []
        roles_data = Roles.query.all()
        response = {
            "error": False,
            "message": "roles list",
            "data": [x.serializer for x in roles_data]
        }
        return response, 201
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        error = error[1:len(error) - 1].split(",")[1]
        response = {
            "error": True,
            "message": error[2:len(error) - 2],
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
        return response, 409

def post_roles(data):
    try:
        if data != None:
            add_role = Roles(
                role_name=data['role_name']
            )
            db.session.add(add_role)
            db.session.commit()
            data = Roles.query.filter_by(role_name=data['role_name']).first()
            response={
                "error": False,
                "message": "roles created",
                "data": data.serializer
            }
            return response
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        error = error[1:len(error) - 1].split(",")[1]
        response = {
            "error": True,
            "message": error[2:len(error) - 2],
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
        return response, 409

def patch_roles(data,args, public_id):
    try:
        data["modified_by"] = public_id
        role_id=None
        if "id" in args.keys() and args["id"] is not None:
            role_id = args["id"]
        else:
            response = {
                "error": True,
                "message": "id not passed",
                "data": None
            }
            return response, 400
        if Roles.query.filter_by(id=role_id).first() is not None:
            Roles.query.filter_by(id=role_id).update(data)
            db.session.commit()
            data = Roles.query.filter_by(id=role_id).first()
            response = {
                "error": False,
                "message": "roles data modified",
                "data": data.serializer
            }
            return response, 200
        else:
            response = {
                "error": True,
                "message": "data not found",
                "data": None
            }
            return response, 404
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        error = error[1:len(error) - 1].split(",")[1]
        response = {
            "error": True,
            "message": error[2:len(error) - 2],
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
        return response, 409
def delete_roles(args):
    try:
        role_id = None
        if "id" in args.keys() and args["id"] is not None:
            role_id = args["id"]
        else:
            response = {
                "error": True,
                "message": "id not passed",
                "data": None
            }
            return response, 404
        data = Roles.query.filter_by(id=role_id).first()
        if data is not None:
            db.session.delete(data)
            db.session.commit()
            roles_data = Roles.query.all()
            response = {
                "error": False,
                "message": "roles deleted",
                "data": [i.serializer for i in roles_data]
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
        error = error[1:len(error) - 1].split(",")[1]
        response = {
            "error": True,
            "message": error[2:len(error) - 2],
            "data": None
        }
        return response, 409
    except Exception as e:
        print("Error: ", e.__repr__())
        response = {
            "error": False,
            "message": "something went wrong",
            "data": None
        }
        return response, 409