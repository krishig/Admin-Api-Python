from app.models import Product_image
from app import db
def post_product_image(data,public_id):
    product_id = data["product_id"]
    for i in data["image_list_url"]:
        product_image_data = Product_image(
            image_url=i["url"],
            image_name=i["file_name"],
            product_id=product_id,
            created_by=public_id
        )
        db.session.add(product_image_data)
        db.session.commit()
    return "Image added in product",200

def delete_product_image(args):
    try:
        data = Product_image.query.filter_by(id=args["id"]).first()
        if data is not None:
            db.session.delete(data)
            db.session.commit()
            return "Data Deleted",200
        else:
            return "Data not found",404
    except Exception as e:
        print("Error: ", e.__repr__())
        return e.__repr__(),409