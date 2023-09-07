from app import db
from app.models import Sub_category
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from sqlalchemy import or_
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='app.log',
                    filemode='a')
def post_sub_category(data,public_id):
    try:
        data_sub_category = Sub_category(
            sub_category_name = data['sub_category_name'],
            category_id = data['category_id'],
            image_url = data['image_url'],
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
        logging.error("409"+"-"+str(e.__dict__['orig']))
        response = {
            "error": True,
            "message": error[2:len(error) - 2],
            "data": None
        }
        return response, 200
    except Exception as e:
        print("Error: ", e.__repr__())
        logging.error("409"+"-"+e.__repr__())
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
                    "data": {"result":sub_category_data.serializer}
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
            paginate_result={}
            sub_category_data = Sub_category.query.order_by(text("id desc")).paginate(page=page_no,per_page=items_per_page)
           # print(category_data[0].sub_category)
            paginate_result["total_pages"]=sub_category_data.pages
            paginate_url="/sub_category?items_per_page=%s&page_number=%s"
            if sub_category_data.has_next==True:
                paginate_result["next_page"]=paginate_url%(items_per_page,page_no+1)
            if sub_category_data.has_prev==True:
                paginate_result["prev_page"] = "/sub_category?items_per_page=%s&page_number=%s" % (items_per_page, page_no - 1)
            if sub_category_data.pages is not None:
                paginate_result["total_pages"]=sub_category_data.pages
            paginate_result["result"]=[x.serializer for x in sub_category_data]
            response = {
                "error": False,
                "message": "list of sub category",
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
            "error": False,
            "message": "something went wrong",
            "data": None
        }
        return response, 409

def search_sub_categories(args,page_no,items_per_page):
    try:
        if "search_sub_category" in args.keys() and args["search_sub_category"] is not None:
            search = "%{}%".format(args['search_sub_category'])
            data = Sub_category.query.filter(Sub_category.sub_category_name.like(search)).paginate(page=page_no,per_page=items_per_page)
            paginate_result= {}
            paginate_url = "/sub_category?items_per_page=%s&page_number=%s"
            if data.has_next==True:
                paginate_result["next_page"] = paginate_url%(items_per_page,page_no+1)
            if data.has_prev==True:
                paginate_result["prev_page"] = paginate_url% (items_per_page, page_no - 1)
            if data.pages is not None:
                paginate_result["total_pages"]=data.pages
            paginate_result["result"] = [i.serializer for i in data]
            response = {
                "error": False,
                "message": "brand search result",
                "data": paginate_result
            }

            return response,200
        else:
            response = {
                "error": True,
                "message": "search_sub_category args not passed in url",
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

def filter_sub_category(category_id,page_no,items_per_page):
    try:
        paginate_result={}
        filters = []
        if "category_id" in category_id.keys() and category_id["category_id"] is not None:
            filters.append((Sub_category.category_id==category_id['category_id']))

        product_data = db.session.query(Sub_category).filter(or_(*filters)).paginate(page=page_no,per_page=items_per_page)
        paginate_result["total_pages"]=product_data.pages
        paginate_url="/sub_category?items_per_page=%s&page_number=%s"
        if product_data.has_next==True:
            paginate_result["next_page"]=paginate_url%(items_per_page,page_no+1)
        if product_data.has_prev==True:
            paginate_result["prev_page"] = paginate_url% (items_per_page, page_no - 1)
        if product_data.pages is not None:
            paginate_result["total_pages"]=product_data.pages
        paginate_result["result"]=[x.serializer for x in product_data]
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
