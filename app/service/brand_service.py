from app.models import Brands
from app import db

def get_brand_details(args):
    try:
        if "id" in args.keys() and args["id"] is not None:
            brand_data = Brands.query.filter_by(id=args["id"]).first()
            return brand_data.serializer,201
        else:
            product_data = Brands.query.all()
           # print(category_data[0].sub_category)
            return [x.serializer for x in product_data], 201
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(), 409
def post_brand(data,public_id):
    try:
        brand_data = Brands(
            brand_name=data["brand_name"],
            brand_image_url=None if "brand_image_id" not in data.keys() or data["brand_image_id"] is None else data["brand_image_id"],
            created_by=public_id
        )
        db.session.add(brand_data)
        db.session.commit()

        return "Brand Created",200
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(), 409

def patch_brand(args,data,public_id):
    try:
        data["modified_by"]=public_id
        id = None
        if "id" in args.keys() and args["id"] is not None:
            id = args["id"]
        else:
            return "id not passed", 400
        brands_data = Brands.query.filter_by(id=id).first()
        if brands_data is not None:
            Brands.query.filter_by(id=id).update(data)
            db.session.commit()
            return "Data Modified", 200
        else:
            return "Data Not found", 404
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(), 409

def delete_brands(args):
    try:
        brand_id = None
        if "id" in args.keys() and args["id"] is not None:
            brand_id = args["id"]
        else:
            return "id not passed", 400
        data = Brands.query.filter_by(id=brand_id).first()
        if data is not None:
            db.session.delete(data)
            db.session.commit()
            return "Data Deleted",200
        else:
            return "Data not found", 404
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(), 409