from app.models import Brands
from app import db
from sqlalchemy.exc import SQLAlchemyError
def get_brand_details(args):
    try:
        if "id" in args.keys() and args["id"] is not None:
            brand_data = Brands.query.filter_by(id=args["id"]).first()
            if brand_data is not None:
                response={
                    "error": False,
                    "message": "details of brand",
                    "data": brand_data.serializer
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
            brands_data = Brands.query.all()
           # print(category_data[0].sub_category)
            response={
                "error": False,
                "message": "list of brands available",
                "data": [x.serializer for x in brands_data]
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
def post_brand(data,public_id):
    try:
        brand_data = Brands(
            brand_name=data["brand_name"],
            brand_image_url=None if "brand_image_url" not in data.keys() or data["brand_image_url"] is None else data["brand_image_url"],
            created_by=public_id
        )
        db.session.add(brand_data)
        db.session.commit()
        brand_data = Brands.query.filter_by(brand_name=data["brand_name"]).first()
        response={
            "error": False,
            "message": "brand created",
            "data": brand_data.serializer
        }
        return response,200
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

def patch_brand(args,data,public_id):
    try:
        data["modified_by"]=public_id
        id = None
        if "id" in args.keys() and args["id"] is not None:
            id = args["id"]
        else:
            response={
                "error": True,
                "message": "id not passed",
                "data": None
            }
            return response, 400
        brands_data = Brands.query.filter_by(id=id).first()
        if brands_data is not None:
            Brands.query.filter_by(id=id).update(data)
            db.session.commit()
            brands_data=Brands.query.filter_by(id=id).first()
            response={
                "error": False,
                "message": "brand data modified",
                "data": brands_data.serializer
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

def delete_brands(args):
    try:
        brand_id = None
        if "id" in args.keys() and args["id"] is not None:
            brand_id = args["id"]
        else:
            response = {
                "error": True,
                "message": "id not passed",
                "data": None
            }
            return response, 400
        data = Brands.query.filter_by(id=brand_id).first()
        if data is not None:
            db.session.delete(data)
            db.session.commit()
            brands_data = Brands.query.all()
            response = {
                "error": False,
                "message": "brand data deleted",
                "data": [i.serializer for i in brands_data]
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
            "error": True,
            "message": "something went wrong",
            "data": None
        }
        return response, 409