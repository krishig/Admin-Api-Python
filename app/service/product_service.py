import json

from app.models import Product, Sub_category
from app import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from sqlalchemy import and_
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='app.log',
                    filemode='a')
def get_product_details(args,page_no,items_per_page):
    try:
        paginate_result = {}
        if "id" in args.keys() and args["id"] is not None:
            product_data = Product.query.filter_by(id=args["id"]).first()
            if product_data is not None:
                response = {
                    "error": False,
                    "message": "product data detail",
                    "data": {
                        "result":product_data.serializer
                    }
                }
                return response, 200
            else:
                response = {
                    "error": True,
                    "message": "data not found",
                    "data": None
                }
                return response, 404
        else:
            product_data = Product.query.order_by(text("id desc")).paginate(page=page_no,per_page=items_per_page)
            paginate_result["total_pages"]=product_data.pages
            paginate_url="/product?items_per_page=%s&page_number=%s"
            if product_data.has_next==True:
                paginate_result["next_page"]=paginate_url%(items_per_page,page_no+1)
            if product_data.has_prev==True:
                paginate_result["prev_page"] = paginate_url % (items_per_page, page_no - 1)
            if product_data.pages is not None:
                paginate_result["total_pages"]=product_data.pages
            paginate_result["result"]=[x.serializer for x in product_data]
            response={
                "error": False,
                "message": "product data list",
                "data": paginate_result
            }
            # print(category_data[0].sub_category)
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

def search_products(args,page_no,items_per_page):
    try:
        if "search_product" in args.keys() and args["search_product"] is not None:
            search = "%{}%".format(args['search_product'])
            data = Product.query.filter(Product.product_name.like(search)).paginate(page=page_no,per_page=items_per_page)
            paginate_result= {}
            paginate_url="/product?items_per_page=%s&page_number=%s"
            if data.has_next==True:
                paginate_result["next_page"]=paginate_url%(items_per_page,page_no+1)
            if data.has_prev==True:
                paginate_result["prev_page"] = paginate_url % (items_per_page, page_no - 1)
            if data.pages is not None:
                paginate_result["total_pages"]=data.pages
            paginate_result["result"] = [i.serializer for i in data]
            response = {
                "error": False,
                "message": "product search result",
                "data": paginate_result
            }

            return response,200
        else:
            response = {
                "error": True,
                "message": "search_product args not passed in url",
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

def filter_products(sub_cat_id,category_id,brand_id,page_no,items_per_page):
    try:

        paginate_result={}
        filters = []
        if "sub_category_id" in sub_cat_id.keys() and sub_cat_id["sub_category_id"] is not None and sub_cat_id["sub_category_id"]!="":
            filters.append(Product.sub_category_id==sub_cat_id["sub_category_id"])
        if "brand_id" in brand_id.keys() and (brand_id["brand_id"] is not None and brand_id["brand_id"]!=""):
            filters.append(Product.brand_id==brand_id["brand_id"])
        if "category_id" in category_id.keys() and category_id["category_id"] is not None and category_id["category_id"]!="":
            print(category_id)
            filters.append((Sub_category.category_id==category_id['category_id']))
        #print(filters)
        #product_data = db.session.query(Product).filter(or_(*filters)).paginate(page=page_no,per_page=items_per_page)
        product_data = db.session.query(Product).outerjoin(Sub_category,Product.sub_category_id==Sub_category.id).filter(and_(*filters)).paginate(page=page_no,per_page=items_per_page)
        #print(product_data)
        paginate_result["total_pages"]=product_data.pages
        paginate_url="/product?items_per_page=%s&page_number=%s"
        if product_data.has_next==True:
            paginate_result["next_page"]=paginate_url%(items_per_page,page_no+1)
        if product_data.has_prev==True:
            paginate_result["prev_page"] = paginate_url % (items_per_page, page_no - 1)
        if product_data.pages is not None:
            paginate_result["total_pages"]=product_data.pages
        paginate_result["result"]=[x.serializer for x in product_data]
        #print(paginate_result)
        response = {
            "error": False,
            "message": "result of filter",
            "data": paginate_result
        }
        return response
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
def post_product(data,user_id):
    try:
        product_data = Product(
            product_name = data["product_name"],
            price=data["price"],
            whole_sale_price=data["whole_sale_price"],
            quantity = data["quantity"],
            discount=data["discount"],
            sub_category_id = data['sub_category_id'],
            brand_id = data['brand_id'],
            product_description=data['product_description'],
            created_by=user_id,
            base_unit = data["base_unit"]
        )
        db.session.add(product_data)
        db.session.commit()
        data = Product.query.filter_by(product_name = data["product_name"]).first()
        response = {
            "error": False,
            "message": "product data added",
            "data": data.serializer
        }
        return response, 200
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

def patch_product(data,args, public_id):
    try:
        data["modified_by"] = public_id
        product_id = None
        if "id" in args.keys() and args["id"] is not None:
            product_id = args["id"]
        else:
            response = {
                "error": True,
                "message": "id not passed",
                "data": None
            }
            return response, 404
        if Product.query.filter_by(id=product_id).first() is not None:
            Product.query.filter_by(id=product_id).update(data)
            db.session.commit()
            product_data = Product.query.filter_by(id=product_id).first()
            response={
                "error": False,
                "message": "product data modified",
                "data": product_data.serializer
            }
            return response,200
        else:
            response = {
                "error": True,
                "message": "no data found",
                "data": None
            }
            return response,404
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

def delete_product(args):
    try:
        product_id = None
        if "id" in args.keys() and args["id"] is not None:
            product_id = args["id"]
        else:
            response = {
                "error": True,
                "message": "id not passed",
                "data": None
            }
            return response, 404
        data = Product.query.filter_by(id=product_id).first()
        if data is not None:
            db.session.delete(data)
            db.session.commit()
            response={
                "error": False,
                "message": "data deleted",
                "data": None
            }
            return response
        else:
            response = {
                "error": False,
                "message": "no data found",
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
