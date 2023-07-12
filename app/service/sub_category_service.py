from app import db
from app.models import Sub_category
from sqlalchemy.exc import SQLAlchemyError
def post_sub_category(data,public_id):
    try:
        data_sub_category = Sub_category(
            sub_category_name = data['sub_category_name'],
            category_id = data['category_id'],
            created_by = public_id
        )
        db.session.add(data_sub_category)
        db.session.commit()
        response = {
            "error": False,
            "message": "sub category created",
            "data": data_sub_category.serializer
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

def get_sub_category_details(args,page_no,items_per_page):
    try:
        if "id" in args.keys() and args["id"] is not None:
            if page_no is not None and items_per_page is not None:
                Sub_category.page_no=page_no
                Sub_category.items_per_page=items_per_page
                if page_no==1:
                    Sub_category.offset = items_per_page
                else:
                    Sub_category.offset=items_per_page+page_no+1
            #obj.product_paginate()
            sub_category_data = Sub_category.query.filter_by(id=args["id"]).first()
            if sub_category_data is not None:
                response = {
                    "error": False,
                    "message": "sub category details",
                    "data": sub_category_data.serializer
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
            Sub_category.page_no=0
            Sub_category.offset=items_per_page
            sub_category_data = Sub_category.query.all()
           # print(category_data[0].sub_category)
            response = {
                "error": False,
                "message": "list of sub category",
                "data": [x.serializer for x in sub_category_data]
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

def patch_sub_category_details(data,args, public_id):
    try:
        sub_category_id = None
        if "id" in args.keys() and args["id"] is not None:
            sub_category_id = args["id"]
        else:
            response = {
                "error": True,
                "message": "id not passed",
                "data": None
            }
            return response, 400
        data["modified_by"] = public_id
        if Sub_category.query.filter_by(id=sub_category_id).first() is not None:
            Sub_category.query.filter_by(id=sub_category_id).update(data)
            db.session.commit()
            data = Sub_category.query.filter_by(id=sub_category_id).first()
            response = {
                "error": False,
                "message": "category data modified",
                "data": data.serializer
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

def delete_sub_category(args):
    try:
        sub_category_id = None
        if "id" in args.keys() and args["id"] is not None:
            sub_category_id = args["id"]
        else:
            response = {
                "error": True,
                "message": "id not passed",
                "data": None
            }
            return response, 404
        data = Sub_category.query.filter_by(id=sub_category_id).first()
        if data is not None:
            db.session.delete(data)
            db.session.commit()
            sub_category_data = Sub_category.query.all()
            response = {
                "error": False,
                "message": "category data deleted",
                "data": [i.serializer for i in sub_category_data]
            }
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