# from werkzeug.datastructures import FileStorage

from app import api,fields,reqparse
token = api.parser()
token.add_argument("Authorization",location='headers')
signup_model = api.model(
    'signup_user',
    {
        'username':fields.String('username',required=True),
        'fullname': fields.String('fullname',required=True),
        'email': fields.String('email',required=True),
        'mobile_number': fields.String('mobile number',required=True),
        'adhaar_number': fields.String('adhaar number',required=True),
        'password': fields.String('password',required=True),
        'House_number': fields.String('House number',required=True),
        'landmark': fields.String('Landmark', required=True),
        'pincode': fields.String('xxxxxx',required=True),
        'city': fields.String('city',required=True),
        'state': fields.String('state',required=True),
        'Role': fields.String('Role',required=True)
    }
)


signup_model_patch = api.model(
    'signup_user_patch',
    {
        'username':fields.String('username'),
        'fullname': fields.String('fullname'),
        'email': fields.String('email'),
        'mobile_number': fields.String('mobile number'),
        'adhaar_number': fields.String('adhaar number'),
        'password': fields.String('password'),
        'House_number': fields.String('House number'),
        'landmark': fields.String('Landmark'),
        'pincode': fields.String('xxxxxx'),
        'city': fields.String('city'),
        'state': fields.String('state'),
        'Role': fields.String('Role')
    }
)

login_model = api.model(
    'login_user',
    {
        'username': fields.String('username',required=True),
        'password': fields.String('password',required=True)
    }
)

role_model=api.model(
    'role_model',
    {
        'role_name':fields.String('role name', required=True)
    }
)

brand_model = api.model(
    'brand_model',
    {
        'brand_name':fields.String('brand name',required=True),
        'brand_image_url': fields.String('image url')
    }
)

brand_model_update=api.model(
    'brand_model_update',
    {
        'brand_name':fields.String('brand name'),
        'brand_image_url': fields.String('image id')
    }
)

category_model = api.model(
    'category_model',
    {
        'category_name': fields.String('Category name',required=True)
    }
)

sub_category_model = api.model(
    'sub_category_model',
    {
        'sub_category_name': fields.String('Sub Category name',required=True),
        "category_id": fields.String("Category Id", required=True),
        "image_url": fields.String("image url")
    }
)
sub_category_model_patch = api.model(
    'sub_category_model',
    {
        'sub_category_name': fields.String('Sub Category name'),
        "category_id": fields.String("Category Id"),
        "image_url": fields.String("image url")
    }
)

product_model = api.model(
    'product_model',
    {
        'product_name': fields.String('product name', required=True),
        'price': fields.String('price', required=True),
        'whole_sale_price': fields.String('dealers price', required=True),
        'base_unit': fields.String("KGorLI",required=True),
        'quantity': fields.String('quantity', required=True),
        'discount': fields.String('discount', required=True),
        'sub_category_id': fields.String('sub category id', required=True),
        'brand_id': fields.String('brand id', required=True),
        'product_description': fields.String('description of the product', required=True)
    }
)

product_model_patch = api.model(
    'product_model',
    {
        'product_name': fields.String('product name'),
        'price': fields.String('price'),
        'whole_sale_price': fields.String('dealers price'),
        'base_unit': fields.String("KGorLI"),
        'quantity': fields.String('quantity'),
        'discount': fields.String('discount'),
        'sub_category_id': fields.String('sub category id'),
        'brand_id': fields.String('brand id'),
        'product_description': fields.String('description of the product')
    }
)
metadata_model = api.model("metadata", {
    'url': fields.String(),
    'file_name': fields.String()
})

image_model = api.model(
    'image_model',
    {
        'product_id': fields.String('product id',required=True),
        'image_list_url': fields.List(fields.Nested(metadata_model),required=True)
    }
)

# image_parser = reqparse.RequestParser()
# image_parser.add_argument('images', type=FileStorage, location='files',action="append")

role_parser = reqparse.RequestParser()
role_parser.add_argument("id",type=int,help="Enter Role id", location='args')

role_parser_req = reqparse.RequestParser()
role_parser_req.add_argument("id",type=int,help="Enter Role id", location='args',required=True)

user_parser = reqparse.RequestParser()
user_parser.add_argument('id',type=int,help='Enter user id',location='args')

user_parser_req = reqparse.RequestParser()
user_parser_req.add_argument('id',type=int,help='Enter user id',location='args',required=True)

brand_parser = reqparse.RequestParser()
brand_parser.add_argument('id',type=int,help='Enter brand id',location='args')

brand_parser_req = reqparse.RequestParser()
brand_parser_req.add_argument('id',type=int,help='Enter brand id',location='args',required=True)

category_parser = reqparse.RequestParser()
category_parser.add_argument('id',type=int,help='Enter category id',location='args')

sub_category_parser = reqparse.RequestParser()
sub_category_parser.add_argument('id',type=int,help='Enter sub category id',location='args')

sub_category_parser_req = reqparse.RequestParser()
sub_category_parser_req.add_argument('id',type=int,help='Enter sub category id',location='args',required=True)

product_parser = reqparse.RequestParser()
product_parser.add_argument('id',type=int,help='Enter the product id',location='args')