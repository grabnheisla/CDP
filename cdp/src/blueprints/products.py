from flask import Blueprint, request
from extensions.tokens import tokens

from main import db

products_bp = Blueprint('products_bp',__name__)


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=True)
    productname = db.Column(db.String(200),nullable=False)
    price = db.Column(db.Integer, default = 0)
    category = db.Column(db.String(200), default="others")
    image = db.Column(db.String(200))

    def toJson(self):
        productJson = {'id':self.id, 'active':self.active, 'productname':self.productname, 'price':self.price, 'category': self.category, 'image':self.image}
        return productJson
    def getPrice(id):
        product = Products.query.get_or_404(id)
        return product.price

@products_bp.route("/products")
def get_products():
    products = Products.query.all()
    output = []
    for product in products:
        output.append(product.toJson())
    return output

@products_bp.route("/products", methods=['POST'])
@tokens.admin_required
def add_product():
    try: bool_active = request.json['active']
    except: bool_active = True
    try: str_name = request.json['productname']
    except: return {"response":"Error Productname missing"}
    try: int_price = request.json['price']
    except: return {"response":"Error Price missing"}
    try: int_price =  int(int_price)
    except: return {"response":"Error Price not an Integer"}
    try: str_category = request.json['category']
    except: str_category = "others"
    try: str_image = request.json['image']
    except: str_image = None
    product = Products(active= bool_active, productname = str_name, price = int_price, category = str_category, image= str_image)
    db.session.add(product)
    db.session.commit()
    return f'"id":"{product.id}"'

@products_bp.route("/products/<id>", methods=['PATCH'])
@tokens.admin_required
def change_product(id):
    product = Products.query.get_or_404(id)
    try: product.active = request.json['active']
    except:  None
    try: product.name = request.json['productname']
    except: None
    try: product.price = request.json['price']
    except: None
    try: product.category = request.json['category']
    except: None
    try: product.image = request.json['image']
    except: None
    db.session.commit()
    return {"response":"Product changed"}

@products_bp.route("/products/<id>")
def get_product(id):
    product = Products.query.get_or_404(id)
    return product.toJson()

@products_bp.route("/products/<id>",methods=['DELETE'])
@tokens.admin_required
def remove_product(id):
    product = Products.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return f'"id":{product.id},"result":"deleted"'
