import boto3
import logging
from app import config
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='app.log',
                    filemode='a')

def get_image_from_bucket():
    try:
        s3 = boto3.resource("s3",region_name = config.slider_bucket_name.region)
        image_obj = s3.Bucket(config.slider_bucket_name.name)
        response={
            "error": False,
            "message": "slider images",
            "data": []
        }
        for x in image_obj.objects.all():
            url = "https://%s.s3.%s.amazonaws.com/%s"%(config.slider_bucket_name.name,config.bucket_name.region,x.key)
            response["data"].append(url)
        return response
    except Exception as e:
        print("Error: ", e.__repr__())
        logging.error("409"+"-"+e.__repr__())
        response = {
            "error": True,
            "message": "something went wrong",
            "data": None
        }
        return response, 409
