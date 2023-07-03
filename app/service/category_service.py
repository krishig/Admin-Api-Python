from app import db
from app.models import Category

def post_category(data,public_id):
    try:
        category_data = Category(
            category_name = data["category_name"],
            created_by = public_id
        )
        db.session.add(category_data)
        db.session.commit()
        return "Category create", 200
    except Exception as e:
        print("Error: ",e.__repr__())
        return e.__repr__()

def get_category_details(args):
    try:
        if "id" in args.keys() and args["id"] is not None:
            category_data = Category.query.filter_by(id=args["id"]).first()
            if category_data is not None:
                return category_data.serializer,201
            else:
                return "No data found",404
        else:
            category_data = Category.query.all()
            if category_data is not None:
           # print(category_data[0].sub_category)
                return [x.serializer for x in category_data],201
            else:
                return "No data found", 404
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(), 409

def patch_category_details(data,args, public_id):
    try:
        data["modified_by"] = public_id
        category_id=None
        if "id" in args.keys() and args["id"] is not None:
            category_id = args["id"]
        else:
            return "id not passed", 400
        if Category.query.filter_by(id=category_id).first() is not None:
            Category.query.filter_by(id=category_id).update(data)
            db.session.commit()
            return "Data Modified",200
        else:
            return "No Data found",404
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(),409

def delete_category(args):
    try:
        category_id = None
        if "id" in args.keys() and args["id"] is not None:
            category_id = args["id"]
        else:
            return "id not passed", 400
        data = Category.query.filter_by(id=category_id).first()
        if data is not None:
            db.session.delete(data)
            db.session.commit()
            return "Category Deleted",200
        else:
            return "Data not found", 404
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(), 409