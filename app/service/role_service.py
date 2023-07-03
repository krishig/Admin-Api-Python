from app.models import Roles
from app import db
def get_role_list():
    try:
        data_list = []
        roles_data = Roles.query.all()
        if roles_data is not None:
            for i in roles_data:
                print(i.users)
                data_list.append(i.serialize)
            return data_list
        else:
            return "Please enter roles from post api", 204
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(),409

def post_roles(data):
    try:
        if data != None:
            add_role = Roles(
                role_name=data['role_name']
            )
            db.session.add(add_role)
            db.session.commit()
            return "role created"
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(),409

def patch_roles(data,args, public_id):
    try:
        data["modified_by"] = public_id
        role_id=None
        if "id" in args.keys() and args["id"] is not None:
            role_id = args["id"]
        else:
            return "id not passed", 400
        if Roles.query.filter_by(id=role_id).first() is not None:
            Roles.query.filter_by(id=role_id).update(data)
            db.session.commit()
            return "Data Modified",200
        else:
            return "No Data found",404
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(),409
def delete_roles(args):
    try:
        role_id = None
        if "id" in args.keys() and args["id"] is not None:
            role_id = args["id"]
        else:
            return "id not passed", 400
        data = Roles.query.filter_by(id=role_id).first()
        if data is not None:
            db.session.delete(data)
            db.session.commit()
            return "Data Deleted",200
        else:
            return "Data not found", 404
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(), 409