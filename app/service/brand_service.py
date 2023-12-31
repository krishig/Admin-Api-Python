from app.models import Brands
from app import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='app.log',
                    filemode='a')
def get_brand_details(args,page_no,items_per_page):
    try:
        if "id" in args.keys() and args["id"] is not None:
            brand_data = Brands.query.filter_by(id=args["id"]).first()
            if brand_data is not None:
                response={
                    "error": False,
                    "message": "details of brand",
                    "data": {"result":brand_data.serializer}
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
            paginate_result={}
            brands_data = Brands.query.order_by(text("id desc")).paginate(page=page_no,per_page=items_per_page)
            paginate_url="/product_brands?items_per_page=%s&page_number=%s"
            if brands_data.has_next==True:
                paginate_result["next_page"]=paginate_url%(items_per_page,page_no+1)
            if brands_data.has_prev==True:
                paginate_result["prev_page"] = paginate_url % (items_per_page, page_no - 1)
            if brands_data.pages is not None:
                paginate_result["total_pages"]=brands_data.pages
            paginate_result["result"]=[x.serializer for x in brands_data]
            response={
                "error": False,
                "message": "list of brands available",
                "data": paginate_result
            }
            return response, 201
    except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            error = error[1:len(error) - 1].split(",")[1]
            logging.error("409"+"-"+str(e.__dict__['orig']))
            response = {
                "error": True,
                "message": error[2:len(error) - 2],
                "data": None
            }
            return response, 409
    except Exception as e:
        print("Error: ", e.__repr__())
        logging.error("409"+"-"+e.__repr__())
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
        logging.error("409"+"-"+str(e.__dict__['orig']))
        response = {
            "error": True,
            "message": error[2:len(error) - 2],
            "data": None
        }
        return response, 409
    except Exception as e:
        print("Error: ", e.__repr__())
        logging.error("409"+"-"+e.__repr__())
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
        logging.error("409"+"-"+str(e.__dict__['orig']))
        response = {
            "error": True,
            "message": error[2:len(error) - 2],
            "data": None
        }
        return response, 409
    except Exception as e:
        print("Error: ", e.__repr__())
        logging.error("409"+"-"+e.__repr__())
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
            logging.error("409"+"-"+str(e.__dict__['orig']))
            response = {
                "error": True,
                "message": error[2:len(error) - 2],
                "data": None
            }
            return response, 409
    except Exception as e:
        print("Error: ", e.__repr__())
        logging.error("409"+"-"+e.__repr__())
        response = {
            "error": True,
            "message": "something went wrong",
            "data": None
        }
        return response, 409

def search_brands(args,page_no,items_per_page):
    try:
        if "search_brand" in args.keys() and args["search_brand"] is not None:
            search = "%{}%".format(args['search_brand'])
            #data = Product.query.filter(Product.sub_category.has(sub_category_name=search)).all(
            data = Brands.query.filter(Brands.brand_name.like(search)).paginate(page=page_no,per_page=items_per_page)
            #print(data)
            paginate_result= {}
            paginate_url="/product_brands?items_per_page=%s&page_number=%s"
            if data.has_next==True:
                paginate_result["next_page"]=paginate_url%(items_per_page,page_no+1)
            if data.has_prev==True:
                paginate_result["prev_page"] = paginate_url % (items_per_page, page_no - 1)
            if data.pages is not None:
                paginate_result["total_pages"]=data.pages
            paginate_result["result"] = [i.serializer for i in data]
            #print(data)

            response = {
                "error": False,
                "message": "brand search result",
                "data": paginate_result
            }

            return response,200
        else:
            response = {
                "error": True,
                "message": "search_brands args not passed in url",
                "data": None
            }
            return response, 400
    except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            error = error[1:len(error) - 1].split(",")[1]
            logging.error("409"+"-"+str(e.__dict__['orig']))
            response = {
                "error": True,
                "message": error[2:len(error) - 2],
                "data": None
            }
            return response, 409
    except Exception as e:
        print("Error: ", e.__repr__())
        logging.error("409"+"-"+e.__repr__())
        response = {
            "error": True,
            "message": "something went wrong",
            "data": None
        }
        return response, 409
