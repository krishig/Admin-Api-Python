import boto3
from app import config
from sqlalchemy.exc import SQLAlchemyError
#image
def delete_image(data):
    try:
        s3 = boto3.resource("s3", region_name=config.bucket_name.region)
        bucket_list = [x.name for x in s3.buckets.all()]
        bucket_name = config.bucket_name.name
        if bucket_name in bucket_list:
            obj = s3.Object(bucket_name=bucket_name, key=data["image_name"]).delete()
        response = {
            "error": False,
            "message": "image removed",
            "data": None
        }
        return response
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