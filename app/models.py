from app import db
from datetime import datetime
from pytz import timezone
from sqlalchemy import func
from sqlalchemy import text
now = datetime.utcnow()
now = now.astimezone(timezone('Asia/Kolkata'))
class Roles(db.Model):
    id = db.Column(db.BigInteger,primary_key=True)
    role_name = db.Column(db.String(20),nullable=False,unique=True)
    created_by = db.Column(db.BigInteger,default=1,nullable=False)
    created_at = db.Column(db.DateTime,default=func.localtime(),nullable=False)
    modified_by = db.Column(db.BigInteger,nullable=True)
    modified_at = db.Column(db.DateTime,onupdate=func.localtime())
    users = db.relationship('Users', backref='roles',uselist=True)

    @property
    def serializer(self):
        return {
            'id': self.id,
            'role_name': self.role_name,
            'users': [x.serializer for x in self.users],
            'created_by': [x for x in db.session.execute(text("select username from users where id=%s"%(self.created_by)))][0][0],
            'created_at': str(self.created_at),
            'modified_by': None if self.modified_by is None else str(self.modified_by),
            'modified_at': None if self.modified_at is None else str(self.modified_at)
        }
class Users(db.Model):
    id = db.Column(db.BigInteger,primary_key=True)
    username = db.Column(db.String(20),nullable=False, unique=True)
    fullname = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(255),nullable=False)
    gender = db.Column(db.String(255),nullable=False)
    mobile_number = db.Column(db.String(13),nullable=False)
    aadhaar_number = db.Column(db.String(12),nullable=False)
    password = db.Column(db.String(255),nullable=False)
    house_number = db.Column(db.String(255),nullable=False)
    landmark = db.Column(db.String(255),nullable=False)
    pincode = db.Column(db.BigInteger,nullable=False)
    district = db.Column(db.String(255),nullable=False)
    city = db.Column(db.String(255),nullable=False)
    state = db.Column(db.String(255),nullable=False)
    Role = db.Column(db.BigInteger,db.ForeignKey('roles.id'))
    created_by = db.Column(db.BigInteger, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=func.localtime(), nullable=False)
    modified_by = db.Column(db.BigInteger, nullable=True)
    modified_at = db.Column(db.DateTime, onupdate=datetime.utcnow().astimezone(timezone('Asia/Kolkata')))



    @property
    def serializer(self):
        return {
            'id': self.id,
            'username': self.username,
            'fullname': self.fullname,
            'email': self.email,
            'mobile_number': self.mobile_number,
            'gender': self.gender,
            'adhaar_number': self.aadhaar_number,
            'password': self.password,
            'House_number': self.house_number,
            'landmark':self.landmark,
            'pincode': self.pincode,
            'city': self.city,
            'district': self.district,
            'state': self.state,
            'Role': self.Role,
            'Role_name': None if self.roles is None else self.roles.role_name,
            'created_by': [x for x in db.session.execute(text("select username from users where id=%s"%(self.created_by)))][0][0],
            'created_at': str(self.created_at),
            'modified_by': None if self.modified_by is None else str(self.modified_by),
            'modified_at': None if self.modified_at is None else str(self.modified_at)
        }

class Brands(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    brand_name = db.Column(db.String(100),nullable=True,unique=True)
    brand_image_url = db.Column(db.Text,nullable=True)
    created_by = db.Column(db.BigInteger, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=func.localtime(), nullable=False)
    modified_by = db.Column(db.BigInteger, nullable=True)
    modified_at = db.Column(db.DateTime, onupdate=func.localtime())
    product = db.relationship('Product', backref='brands')

    @property
    def serializer(self):
        return {
            "id": self.id,
            "brand_name": self.brand_name,
            "brand_image_url": self.brand_image_url,
            "products": [x.serializer for x in self.product],
            'created_by': [x for x in db.session.execute(text("select username from users where id=%s"%(self.created_by)))][0][0],
            'created_at': str(self.created_at),
            'modified_by': None if self.modified_by is None else str(self.modified_by),
            'modified_at': None if self.modified_at is None else str(self.modified_at)
        }

class Product_image(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    image_url = db.Column(db.String(500),nullable=True)
    image_name = db.Column(db.String(255),nullable=True)
    product_id = db.Column(db.BigInteger,db.ForeignKey('product.id'))
    created_by = db.Column(db.BigInteger, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=func.localtime(), nullable=False)
    modified_by = db.Column(db.BigInteger, nullable=True)
    modified_at = db.Column(db.DateTime, onupdate=func.localtime())
    @property
    def serializer(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "image_name": self.image_name,
           # 'product_id': self.product.id,
           # 'brand_name': self.product.brand_name,
            'created_by': [x for x in db.session.execute(text("select username from users where id=%s"%(self.created_by)))][0][0],
            'created_at': str(self.created_at),
            'modified_by': None if self.modified_by is None else str(self.modified_by),
            'modified_at': None if self.modified_at is None else str(self.modified_at)
        }

class Category(db.Model):
    id = db.Column(db.BigInteger,primary_key=True)
    category_name = db.Column(db.String(255),nullable=False,unique=True)
    created_by = db.Column(db.BigInteger, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=func.localtime(), nullable=False)
    modified_by = db.Column(db.BigInteger, nullable=True)
    modified_at = db.Column(db.DateTime, onupdate=func.localtime())
    sub_category = db.relationship('Sub_category', backref='category')

    @property
    def serializer(self):
        return {
            "id": self.id,
            "category_name": self.category_name,
            "sub_category": [x.serializer for x in self.sub_category],
            'created_by': [x for x in db.session.execute(text("select username from users where id=%s"%(self.created_by)))][0][0],
            'created_at': str(self.created_at),
            'modified_by': None if self.modified_by is None else str(self.modified_by),
            'modified_at': None if self.modified_at is None else str(self.modified_at)
        }

class Sub_category(db.Model):

    page_no = 0
    items_per_page=10
    offset=items_per_page
    id = db.Column(db.BigInteger,primary_key=True)
    sub_category_name = db.Column(db.String(255),nullable=False,unique=True)
    category_id = db.Column(db.BigInteger, db.ForeignKey('category.id'))
    image_url = db.Column(db.Text,nullable=True)
    created_by = db.Column(db.BigInteger, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=func.localtime(), nullable=False)
    modified_by = db.Column(db.BigInteger, nullable=True)
    modified_at = db.Column(db.DateTime, onupdate=func.localtime())

    product = db.relationship('Product', backref='sub_category')
    @property
    def serializer(self):
        return {
            "id": self.id,
            "sub_category_name": self.sub_category_name,
            "sub_category_image": self.image_url,
            "category_name": None if self.category is None else self.category.category_name,
            "image_url": self.image_url,
            #"products": [x.serializer for x in self.product[(Sub_category.page_no-1)*
            "products": [x.serializer for x in self.product],
            #"page_number":self.page_no,
            #"total_product_pages": len(self.product)//Sub_category.items_per_page,
            'created_by': [x for x in db.session.execute(text("select username from users where id=%s"%(self.created_by)))][0][0],
            'created_at': str(self.created_at),
            'modified_by': None if self.modified_by is None else str(self.modified_by),
            'modified_at': None if self.modified_at is None else str(self.modified_at)
        }

class Product(db.Model):
    id = db.Column(db.BigInteger,primary_key=True)
    product_name = db.Column(db.String(255),nullable=False)
    whole_sale_price=db.Column(db.BigInteger,nullable=False)
    price = db.Column(db.BigInteger,nullable=False)
    quantity = db.Column(db.BigInteger,nullable=False)
    base_unit = db.Column(db.String(250),nullable=False)
    discount = db.Column(db.BigInteger,nullable=False)
    sub_category_id = db.Column(db.BigInteger,db.ForeignKey('sub_category.id'))
    brand_id = db.Column(db.BigInteger,db.ForeignKey('brands.id'))
    product_description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.BigInteger, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=func.localtime(), nullable=False)
    modified_by = db.Column(db.BigInteger, nullable=True)
    modified_at = db.Column(db.DateTime, onupdate=func.localtime())
    product_image = db.relationship('Product_image', backref='product')
    #order_items = db.relationship('Order_items', backref='product',uselist=False)
    @property
    def serializer(self):
        return {
        "id": self.id,
        "product_name": self.product_name,
        "whole_sale_price": self.whole_sale_price,
        "price": self.price,
        "quantity": self.quantity,
        "base_unit": self.base_unit,
        "discount": self.discount,
        "sub_category_id": self.sub_category_id,
        "category_id": None if self.modified_by is None else self.sub_category.category_id,
        "sub_category_name": None if self.sub_category is None else self.sub_category.sub_category_name,
        "brand_id": self.brand_id,
        "brand_name": None if self.brands is None else self.brands.brand_name,
        "product_description": self.product_description,
        "product_image": [x.serializer for x in self.product_image],
        'created_by': [x for x in db.session.execute(text("select username from users where id=%s"%(self.created_by)))][0][0],
        'created_at': str(self.created_at),
        'modified_by': None if self.modified_by is None else str(self.modified_by),
        'modified_at': None if self.modified_at is None else str(self.modified_at)
        }

# class Orders(db.Model):
#     id = db.Column(db.BigInteger,primary_key=True),
#     customer_id =db.Column(db.BigInteger,nullable=False)
#     order_id = db.Column(db.String,nullable=False)
#     created_by = db.Column(db.BigInteger, default=1, nullable=False)
#     created_at = db.Column(db.DateTime, default=now, nullable=False)
#     modified_by = db.Column(db.BigInteger, nullable=True)
#     modified_at = db.Column(db.DateTime, onupdate=now)
# class Order_items(db.Model):
#     id = db.Column(db.BigInteger,primary_key=True),
#     price_after_discount=db.Column(db.Integer,nullable=False),
#     totalProductDiscountPrice=db.Column(db.Integer,nullable=False)
#     quantity=db.Column(db.BigInteger,nullable=False),
#     order_id = db.Column(db.BigInteger,nullable=False),
#     product_id = db.Column(db.BigInteger,db.ForeignKey('product.id')),
#     created_by = db.Column(db.BigInteger, default=1, nullable=False)
#     created_at = db.Column(db.DateTime, default=now, nullable=False)
#     modified_by = db.Column(db.BigInteger, nullable=True)
#     modified_at = db.Column(db.DateTime, onupdate=now)
