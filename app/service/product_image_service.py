from app.models import Product_image
from app import db
import boto3
from app.models import Product
from sqlalchemy.exc import SQLAlchemyError
from app import config
def post_product_image(data,public_id):
    try:
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
        data = Product.query.filter_by(id=product_id).first()
        response={
            "error": False,
            "message": "image added in product",
            "data": data.serializer
        }
        return response,200
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        error = error[1:len(error)-1].split(",")[1]
        response = {
            "error": True,
            "message": error[2:len(error)-2],
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

def delete_product_image(args):
    try:
        data = Product_image.query.filter_by(id=args["id"]).first()
        if data is not None:
            db.session.delete(data)
            db.session.commit()
            s3 = boto3.resource("s3", region_name=config.bucket_name.region)
            bucket_list = [x.name for x in s3.buckets.all()]
            bucket_name = config.bucket_name.name
            if bucket_name in bucket_list:
                obj = s3.Object(bucket_name=bucket_name, key=data.image_name).delete()
            data = Product.query.filter_by(id=data.product_id).first()
            response = {
                "error": False,
                "message": "image removed",
                "data": {"result":data.serializer}
            }
            return response
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
