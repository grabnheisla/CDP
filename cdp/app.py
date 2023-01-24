from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB')
migrate = Migrate()
db = SQLAlchemy(app)
migrate.init_app(app,db)


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=True)
    favorite = db.Column(db.Boolean, default=True)
    firstname = db.Column(db.String(200))
    lastname = db.Column(db.String(200))
    falseLogonCount = db.Column(db.Integer, nullable=False, default=0)
    password = db.Column(db.String(200))
    salt = db.Column(db.String(200))
    username = db.Column(db.String(200),unique=True,nullable=False)
    displayname = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200))
    balance = db.Column(db.Integer, default=0)
    created_on = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    def __repr__(self):
        return f'{{"id": {self.id},"username":{self.username}}}'
    def __str__(self):
        return "{{'id':{self.id},'active':{self.active},'favorite':{self.favorite},'firstname':{self.firstname},'lastname':{self.lastname},'username':{self.username},'displayname':{self.displayname},'email':{self.email},'balance':{self.balance},'created_on':{self.created_on},'last_login':{self.last_login}, 'falseLogonCount':{self.falseLogonCount}}}"
    def toJson(self):
        userJson = {'id': self.id, 'active':self.active,'favorite':self.favorite,'firstname':self.firstname,'lastname':self.lastname,'username':self.username,'displayname':self.displayname,'email':self.email,'balance':self.balance,'created_on':self.created_on,'last_login':self.last_login, 'falseLogonCount':self.falseLogonCount}
        return userJson

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/users")
def get_users():
    users = Users.query.all()
    output = []
    for user in users:
        user_data = user.toJson()
        #user_data = {'id':user.id,'username':user.username,'displayname':user.displayname,'email':user.email,'balance':user.balance,'created_on':user.created_on,'last_logon':user.last_login}
        output.append(user_data)

    return output
@app.route("/users/<id>")
def get_user(id):
    user = Users.query.get_or_404(id)
    return user.toJson()

@app.route("/users", methods=['POST'])
def add_user():
    try: str_first = request.json['firstname'] 
    except: str_first = None
    try: str_last = request.json['lastname']
    except: str_last = None
    try: bool_fav = request.json['favorite']
    except: bool_fav = True
    try: str_mail = request.json['email']
    except: str_mail = None
    user = Users(username=request.json['username'],displayname=request.json['displayname'],firstname=str_first, lastname=str_last, favorite=bool_fav,  email=str_mail, created_on=datetime.now())
    db.session.add(user)
    db.session.commit()
    return f'"id":"{user.id}"'

@app.route("/users/<id>", methods=['DELETE'])
def delete_user(id):
    user = Users.query.get_or_404(id)
    if user is None:
        return {"response":"Not found"}
    db.session.delete(user)
    db.session.commit()
    return f'"id":{user.id},"result":"deleted"'


class Payments(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.ForeignKey(Users.id))
    amount = db.Column(db.Integer, default = 0)
    type = db.Column(db.String(200), default = 'cash')
    timestamp = db.Column(db.DateTime)

    def toJson(self):
        paymentJson = {'id':self.id, 'userid':self.userid, 'amount': self.amount, 'type': self.type, 'timestamp': self.timestamp}
        return paymentJson
@app.route("/payments")
def get_payments():
    payments = Payments.query.all()
    output = []
    for payment in payments:
        output.append(payment.toJson())
    return output
@app.route("/payments/<id>")
def get_payment(id):
    payment = Payments.query.get(id)
    return payment.toJson()

@app.route("/payments", methods=['POST'])
def add_payment():
    try: uid = request.json['userid'] 
    except: return {"response":"User not found!"}
    try: amount = request.json['amount']
    except: return {"response":"Amount missing!"}
    try: int(amount)
    except: return {"response":"Amount is not a digit!"}
    try: str_type = request.json['type']
    except: str_type = None
    user = Users.query.get(uid)
    user.balance = user.balance + int(amount)
    
    payment = Payments(userid = uid, amount= amount, type=str_type, timestamp=datetime.now())
    db.session.add(payment)
    db.session.commit()
    return f'"id":"{payment.id}"'

@app.route("/payments/<id>", methods=['DELETE'])
def delete_payment(id):
    payment = Payments.query.get_or_404(id)
    user = Users.query.get(payment.userid)
    user.balance = user.balance - payment.amount
    db.session.delete(payment)
    db.session.commit()
    return f'"id":{payment.id},"result":"deleted"'

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


@app.route("/products")
def get_products():
    products = Products.query.all()
    output = []
    for product in products:
        output.append(product.toJson())
    return output

@app.route("/products", methods=['POST'])
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

@app.route("/products/<id>", methods=['PATCH'])
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

@app.route("/products/<id>")
def get_product(id):
    product = Products.query.get_or_404(id)
    return product.toJson()


class Purchases(db.Model):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    purchaseid = db.Column(db.Integer, nullable = False) # --> Summarizes one Purchase of different Products
    userid = db.Column(db.ForeignKey(Users.id))
    productid = db.Column(db.ForeignKey(Products.id))
    amount = db.Column(db.Integer, default=1, nullable= False)
    timestamp = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def toJson(self):
        purchaseJson = {'id':self.id, 'purchaseid':self.purchaseid, 'userid':self.userid, 'productid':self.productid, 'amount': self.amount, 'timestamp': self.timestamp}
        return purchaseJson

@app.route("/purchases")
def get_purchases():
    purchases = Purchases.query.all()
    output = []
    for purchase in purchases:
        output.append(purchase.toJson())
    return output

@app.route("/purchases", methods=['POST'])
def add_purchase():
    try: int_purchid = request.json['purchaseid']
    except: 
        try: 
            last_purchid = Purchases.query.order_by(Purchases.purchaseid.desc()).first()
            int_purchid = last_purchid.purchaseid+1
        except: int_purchid = 0
    try: uid = request.json['userid']
    except: return {"response":"Error - No userid defined"}
    try: uid = int(uid)
    except: return {"response":"Error - Userid not integer"}
    if Users.query.get(uid) == None:
        return {"response":"Error - User not found"}
    try: prodid = request.json['productid']
    except: return {"response":"Error - No productid defined"}
    try: prodid = int(prodid)
    except: return {"response":"Error - Productid not integer"}
    if Products.query.get(prodid) == None:
        return {"response":"Error - Product not found"}
    try: int_amount = request.json['amount']
    except: int_amount = 1
    purchase = Purchases(purchaseid = int_purchid, userid = uid, productid=prodid, amount=int_amount, timestamp = datetime.now() )

    ## TO DO ##
    # Calculate Purchase and remove money from user!
    ###
    db.session.add(purchase)
    db.session.commit()
    return f'"id":"{purchase.id}"'


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=port)
    