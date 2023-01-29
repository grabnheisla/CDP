from flask import Blueprint, request
from extensions.tokens import tokens
from datetime import datetime

from main import db

from blueprints.users import Users
from blueprints.products import Products

purchases_bp = Blueprint('purchases_bp',__name__)




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

@purchases_bp.route("/purchases")
def get_purchases():
    purchases = Purchases.query.all()
    output = []
    for purchase in purchases:
        output.append(purchase.toJson())
    return output

@purchases_bp.route("/purchases", methods=['POST'])
@tokens.token_required
def add_purchase():
    try: 
        last_purchid = Purchases.query.order_by(Purchases.purchaseid.desc()).first()
        int_purchid = last_purchid.purchaseid+1
    except: int_purchid = 0
    json = request.get_json()
    try: uid = json['userid']
    except: return {"response":"Userid must be set!"},400
    try: products = json['products']
    except: return {"response":"No products set!"},400
    price = 0
    for product in products:
        try: prodid = product['productid']
        except: return {"response":"No productid set!"},400
        try: int_amount = product['amount']
        except: int_amount = 1
        purchase = Purchases(purchaseid = int_purchid, userid = uid, productid=prodid, amount=int_amount, timestamp = datetime.now() )
        db.session.add(purchase)
        price += Products.getPrice(prodid)*int_amount
    
    Users.debit(uid,price)
    db.session.commit()
    return {"id":purchase.id,"price":price}

