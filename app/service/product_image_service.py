from app.models import Product_image
from app import db
def post_product_image(data,public_id):
    product_id = data["product_id"]
    for i in data["image_list_url"]:
        product_image_data = Product_image(
            image_url=i["url"],
            image_name=i["file_name"],
            product_id=product_id
        )
        db.session.add(product_image_data)
        db.session.commit()
    return "Image added in product",200