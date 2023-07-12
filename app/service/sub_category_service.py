from app import db
from app.models import Sub_category
def post_sub_category(data,public_id):
    try:
        data_sub_category = Sub_category(
            sub_category_name = data['sub_category_name'],
            category_id = data['category_id'],
            created_by = public_id
        )
        db.session.add(data_sub_category)
        db.session.commit()
        return data_sub_category.serializer, 200
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(), 409

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
            return sub_category_data.serializer,201
        else:
            Sub_category.page_no=0
            Sub_category.offset=items_per_page
            sub_category_data = Sub_category.query.all()
           # print(category_data[0].sub_category)
            return [x.serializer for x in sub_category_data], 201
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(), 409

def patch_sub_category_details(data,args, public_id):
    try:
        sub_category_id = None
        if "id" in args.keys() and args["id"] is not None:
            sub_category_id = args["id"]
        else:
            return "id not passed", 400
        data["modified_by"] = public_id
        if Sub_category.query.filter_by(id=sub_category_id).first() is not None:
            Sub_category.query.filter_by(id=sub_category_id).update(data)
            db.session.commit()
            return "Data Modified",200
        else:
            return "No Data found",404
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(),409

def delete_sub_category(args):
    try:
        sub_category_id = None
        if "id" in args.keys() and args["id"] is not None:
            sub_category_id = args["id"]
        else:
            return "id not passed", 400
        data = Sub_category.query.filter_by(id=sub_category_id).first()
        if data is not None:
            db.session.delete(data)
            db.session.commit()
            return "Data Deleted",200
        else:
            return "Data not found", 404
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(), 409