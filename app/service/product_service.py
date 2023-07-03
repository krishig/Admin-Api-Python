from app.models import Product
from app import db

def get_product_details(args):
    try:
        if "id" in args.keys() and args["id"] is not None:
            product_data = Product.query.filter_by(id=args["id"]).first()
            return product_data.serializer,201
        else:
            product_data = Product.query.all()
           # print(category_data[0].sub_category)
            return [x.serializer for x in product_data], 201
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(), 409
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
        return data.serializer, 200
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(), 409

def patch_product(data,args, public_id):
    try:
        data["modified_by"] = public_id
        product_id = None
        if "id" in args.keys() and args["id"] is not None:
            product_id = args["id"]
        else:
            return "id not passed", 400
        if Product.query.filter_by(id=product_id).first() is not None:
            Product.query.filter_by(id=product_id).update(data)
            db.session.commit()
            return "Data Modified",200
        else:
            return "No Data found",404
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(),409

def delete_product(args):
    try:
        product_id = None
        if "id" in args.keys() and args["id"] is not None:
            product_id = args["id"]
        else:
            return "id not passed", 400
        data = Product.query.filter_by(id=product_id).first()
        if data is not None:
            db.session.delete(data)
            db.session.commit()
        else:
            return "Data not found", 404
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(), 409