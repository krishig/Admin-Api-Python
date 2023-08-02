from app import app,api,request,db,config
from app import Resource, fields,Namespace
from app.route_var import signup_model, signup_model_patch, login_model, role_model, user_parser, brand_model, brand_model_update, token, \
    brand_parser,brand_parser_req, category_model, category_parser, sub_category_model,sub_category_parser,sub_category_model_patch,\
    product_model,product_parser,product_model_patch,image_model,role_parser_req,role_parser,user_parser_req, \
    sub_category_parser_req,image_id_parser,page_number,items_per_page,image_url_parser,search_product,search_brand,search_sub_category,\
    filter_product_sub_category_id,filter_product_brand_id,search_user,filter_product_category_id
from app.models import Users,Roles,Brands
from app.service.product_image_service import post_product_image,delete_product_image
from app.service.role_service import get_role_list,post_roles,delete_roles,patch_roles
from app.service.user_service import get_users_list, post_user_details, patch_users, delete_users, search_users
from app.service.user_login_service import post_user_login,token_required
from app.service.brand_service import get_brand_details, post_brand, patch_brand, delete_brands, search_brands
from app.service.category_service import post_category, get_category_details,patch_category_details,delete_category
from app.service.sub_category_service import post_sub_category, get_sub_category_details, patch_sub_category_details, \
    delete_sub_category, search_sub_categories
from app.service.product_service import post_product, patch_product, get_product_details, delete_product, \
    search_products, filter_products
from app.service.delete_image_from_s3 import delete_image
from sqlalchemy import exc
import boto3
import os
from datetime import datetime
#ns = Namespace("orders",description="Api's related to orders")
@api.route('/user_role')
class user_role(Resource):

    @api.expect(role_parser)
    def get(self):
        try:
            return get_role_list(), 200
        except Exception as e:
            return e.__repr__()

    @api.expect(role_model)
    def post(self):
        data = api.payload
        return post_roles(data=data),201

    @api.expect(role_parser_req, validate=True)
    def delete(self):
        args = role_parser_req.parse_args()
        return delete_roles(args=args)

    @api.expect(role_parser_req, role_model,token, validate=True)
    @token_required
    def patch(current_user,self):
        args = role_parser_req.parse_args()
        data = api.payload
        return patch_roles(args=args, data=data, public_id=current_user.id)

@api.route('/user')
class user(Resource):
    @api.expect(items_per_page,page_number,user_parser,token)
    @token_required
    def get(current_user,self):
        args = user_parser.parse_args()
        page_no = page_number.parse_args()
        rows_per_page = items_per_page.parse_args()
        return get_users_list(args, page_no=page_no['page_number'], items_per_page=rows_per_page['items_per_page'])

    @api.expect(signup_model,validate=True)
    def post(self):
        try:
            data = api.payload
            return post_user_details(data)
        except exc.SQLAlchemyError as e:
            return e.__repr__()

    @api.expect(user_parser_req,signup_model_patch, token,validate=True)
    @token_required
    def patch(current_user,self):
        args = user_parser_req.parse_args()
        data = api.payload
        return patch_users(data=data, args=args, public_id=current_user.id)

    @api.expect(user_parser_req, token,validate=True)
    @token_required
    def delete(current_user,self):
        args = user_parser_req.parse_args()
        return delete_users(args=args)


@api.route('/user/login')
class user_login(Resource):
    @api.expect(login_model)
    def post(self):
        auth = api.payload
        return post_user_login(auth)

@api.route('/product_brands')
class product_brands(Resource):

    @api.expect(brand_parser,items_per_page,page_number,token,validate=True)
    @token_required
    def get(current_user,self):
        args = brand_parser.parse_args()
        page_no = page_number.parse_args()
        rows_per_page = items_per_page.parse_args()
        return get_brand_details(args=args,page_no=page_no['page_number'],items_per_page=rows_per_page['items_per_page'])

    @api.expect(brand_model,token,validate=True)
    @token_required
    def post(current_user,self):
        data = api.payload
        return post_brand(data =data,public_id = current_user.id)

    @api.expect(brand_model_update,brand_parser_req,token,validate=True)
    @token_required
    def patch(current_user,self):
        args = brand_parser_req.parse_args()
        data= api.payload
        return patch_brand(args=args,data=data,public_id=current_user.id)

    @api.expect(brand_parser_req,token,validate=True)
    @token_required
    def delete(current_user,self):
        args = brand_parser_req.parse_args()
        return delete_brands(args)

@api.route('/categories')
class categories(Resource):
    @api.expect(category_parser,token)
    @token_required
    def get(current_user,self):
        args = category_parser.parse_args()
        return get_category_details(args=args)

    @api.expect(category_model,token,validate=True)
    @token_required
    def post(current_user,self):
        data = api.payload
        return post_category(data=data,public_id=current_user.id)

    @api.expect(category_parser,category_model, token,validate=True)
    @token_required
    def patch(current_user, self):
        args = category_parser.parse_args()
        data = api.payload
        return patch_category_details(data =data,args=args,public_id = current_user.id)

    @api.expect(category_parser,token,validate=True)
    @token_required
    def delete(current_user,self):
        args = category_parser.parse_args()
        return delete_category(args=args)

@api.route('/sub_category')
class sub_category(Resource):
    @api.expect(sub_category_parser,items_per_page,page_number,token,validate=True)
    @token_required
    def get(current_user,self):
        args = sub_category_parser.parse_args()
        page_no = page_number.parse_args()
        rows_per_page = items_per_page.parse_args()
        return get_sub_category_details(args=args,page_no=page_no['page_number'],items_per_page=rows_per_page['items_per_page'])

    @api.expect(sub_category_model, token, validate=True)
    @token_required
    def post(current_user,self):
        data = api.payload
        return post_sub_category(data=data,public_id=current_user.id)

    @api.expect(sub_category_model_patch, sub_category_parser_req, token, validate=True)
    @token_required
    def patch(current_user, self):
        args = sub_category_parser.parse_args()
        data = api.payload
        return patch_sub_category_details(data=data, args=args, public_id=current_user.id)

    @api.expect(sub_category_parser_req,token,validate=True)
    @token_required
    def delete(current_user,self):
        args = category_parser.parse_args()
        return delete_sub_category(args=args)

@api.route('/subcategory/delete_image')
class delete_subcategory(Resource):
    @api.expect(image_url_parser,token,validate=True)
    def delete(self):
        args = image_url_parser.parse_args()
        return delete_image(args)


@api.route('/product')
class products(Resource):

    @api.expect(product_parser,items_per_page,page_number,token, validate=True)
    @token_required
    def get(current_user,self):
        args = product_parser.parse_args()
        page_no = page_number.parse_args()
        rows_per_page = items_per_page.parse_args()
        #print(rows_per_page,page_no)
        return get_product_details(args=args,page_no=page_no['page_number'],items_per_page=rows_per_page['items_per_page'])

    @api.expect(product_model,token,validate=True)
    @token_required
    def post(current_user,self):
        data = api.payload
        return post_product(data=data,user_id=current_user.id)

    @api.expect(product_parser,product_model_patch, token, validate=True)
    @token_required
    def patch(current_user, self):
        args = product_parser.parse_args()
        data = api.payload
        return patch_product(data=data, args=args,public_id=current_user.id)

    @api.expect(product_parser,token,validate=True)
    @token_required
    def delete(current_user,self):
        args = product_parser.parse_args()
        return delete_product(args=args)

@api.route('/product/search')
class product_search(Resource):

    @api.expect(search_product,items_per_page,page_number,token,vaildate=True)
    @token_required
    def get(current_user,self):
        args = search_product.parse_args()
        page_no = page_number.parse_args()
        rows_per_page = items_per_page.parse_args()
        return search_products(args=args,page_no=page_no['page_number'],items_per_page=rows_per_page['items_per_page'])

@api.route('/product_brand/search')
class product_brand_search(Resource):

    @api.expect(items_per_page,page_number,token,search_brand,token,vaildate=True)
    @token_required
    def get(current_user,self):
        args = search_brand.parse_args()

        page_no = page_number.parse_args()
        rows_per_page = items_per_page.parse_args()
        return search_brands(args=args,page_no=page_no['page_number'],items_per_page=rows_per_page['items_per_page'])

@api.route('/sub_category/search')
class sub_category_search(Resource):

    @api.expect(items_per_page,page_number,token,search_sub_category,token,vaildate=True)
    @token_required
    def get(current_user,self):
        args = search_sub_category.parse_args()
        page_no = page_number.parse_args()
        rows_per_page = items_per_page.parse_args()
        return search_sub_categories(args=args,page_no=page_no['page_number'],items_per_page=rows_per_page['items_per_page'])

@api.route('/user/search')
class user_search(Resource):

    @api.expect(items_per_page,page_number,token,search_user,token,vaildate=True)
    @token_required
    def get(current_user,self):
        args = search_user.parse_args()
        page_no = page_number.parse_args()
        rows_per_page = items_per_page.parse_args()
        return search_users(args=args,page_no=page_no['page_number'],items_per_page=rows_per_page['items_per_page'])

@api.route('/product/filter')
class product_filter(Resource):
    @api.expect(items_per_page,page_number,filter_product_category_id,filter_product_sub_category_id,filter_product_brand_id,token,validate=True)
    @token_required
    def get(current_user,self):
        sub_category_id = filter_product_sub_category_id.parse_args()
        brand_id = filter_product_brand_id.parse_args()
        category_id = filter_product_category_id.parse_args()
        page_no = page_number.parse_args()
        rows_per_page = items_per_page.parse_args()
        return filter_products(sub_cat_id=sub_category_id,category_id=category_id,brand_id=brand_id,page_no=page_no['page_number'],items_per_page=rows_per_page['items_per_page'])
@api.route('/image')
class image_upload(Resource):

    @api.expect(token,validate=True)
    @token_required
    def post(current_user,self):
        data=[]
        allowed_extension = ['png','jpeg','jpg']
        # if "multipart/form-data" in request.headers['Content-Type']:
        files = request.files.getlist("filename")
        for file in files:
            ext = file.filename.split(".")[1]
            #if ext in allowed_extension:
            result={}
            #file.save(file.filename)
            file_name=file.filename
            s3 = boto3.resource("s3",region_name = config.bucket_name.region)
            bucket_list= [x.name for x in s3.buckets.all()]
            bucket_name = config.bucket_name.name
            print(bucket_list)
            if bucket_name in bucket_list:
                loc = "./temp"

                file.save("".join([loc,file_name]))
                s3_key_file= "".join([str(datetime.now()),file_name])
                s3.Bucket(bucket_name).upload_file(Filename="".join([loc,file_name]), Key=s3_key_file)
                os.remove("".join([loc,file_name]))
                image_s3_url= "https://krishig.s3.%s.amazonaws.com/%s"%(config.bucket_name.region,s3_key_file)
                result["file_name"]=file_name
                result["url"]=image_s3_url
                data.append(result)
            # else:
            #     response = {
            #         "error": False,
            #         "message": "plz select png,jpeg,jpg extension file",
            #         "data": None
            #     }
            #return response
            response = {
                "error": False,
                "message": "Image uploaded",
                "data": data
            }
        return response,200
        # else:
        #     return "Wrong Content-Type"
@api.route("/product_image")
class product_image(Resource):
    @api.expect(image_model,token,validate=True)
    @token_required
    def post(current_user,self):
        data = api.payload
        return post_product_image(data=data,public_id=current_user.id)

    @api.expect(image_id_parser,token,validate=True)
    @token_required
    def delete(current_user,self):
        args = image_id_parser.parse_args()
        return delete_product_image(args=args)

class generate_otp(Resource):

    @api.expect(token,validate=True)
    def get(self):
        pass
