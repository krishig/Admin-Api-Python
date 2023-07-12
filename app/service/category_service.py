from app import db
from app.models import Category
from sqlalchemy.exc import SQLAlchemyError
def post_category(data,public_id):
    try:
        category_data = Category(
            category_name = data["category_name"],
            created_by = public_id
        )
        db.session.add(category_data)
        db.session.commit()
        category_data = Category.query.filter_by(category_name=data["category_name"]).first()
        response  = {
            "error": False,
            "message": "category created",
            "data": category_data.serializer
        }
        return response, 200
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


def get_category_details(args):
    try:
        if "id" in args.keys() and args["id"] is not None:
            category_data = Category.query.filter_by(id=args["id"]).first()
            if category_data is not None:
                response = {
                    "error": False,
                    "message": "details of brand",
                    "data": category_data.serializer
                }
                return response,201
            else:
                response = {
                    "error": True,
                    "message": "no data found",
                    "data": None
                }
                return response, 404
        else:
            category_data = Category.query.all()
           # print(category_data[0].sub_category)
            response = {
                "error": False,
                "message": "details of category",
                "data": [x.serializer for x in category_data]
            }
            return response,201
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
        return response, 409

def patch_category_details(data,args, public_id):
    try:
        data["modified_by"] = public_id
        category_id=None
        if "id" in args.keys() and args["id"] is not None:
            category_id = args["id"]
        else:
            response = {
                "error": True,
                "message": "id not passed",
                "data": None
            }
            return response, 400
        if Category.query.filter_by(id=category_id).first() is not None:
            Category.query.filter_by(id=category_id).update(data)
            db.session.commit()
            category_data = Category.query.filter_by(id=category_id).first()
            response={
                "error": False,
                "message": "category data modified",
                "data": category_data.serializer
            }
            return response,200
        else:
            response = {
                "error": True,
                "message": "data not found",
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
        return response, 409

def delete_category(args):
    try:
        category_id = None
        if "id" in args.keys() and args["id"] is not None:
            category_id = args["id"]
        else:
            response = {
                "error": True,
                "message": "id not passed",
                "data": None
            }
            return response, 404
        data = Category.query.filter_by(id=category_id).first()
        if data is not None:
            db.session.delete(data)
            db.session.commit()
            category_data = Category.query.all()
            response = {
                "error": False,
                "message": "category data deleted",
                "data": [i.serializer for i in category_data]
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
        response = {
            "error": False,
            "message": "something went wrong",
            "data": None
        }
        return response, 409