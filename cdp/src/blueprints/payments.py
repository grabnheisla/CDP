from flask import Blueprint, request
from extensions.tokens import tokens
import datetime

from main import db
from blueprints.users import Users

payments_bp = Blueprint('payments_bp',__name__)


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
@payments_bp.route("/payments")
@tokens.token_required
def get_payments():
    payments = Payments.query.all()
    output = []
    for payment in payments:
        output.append(payment.toJson())
    return output
@payments_bp.route("/payments/<id>")
def get_payment(id):
    payment = Payments.query.get(id)
    return payment.toJson()

@payments_bp.route("/payments", methods=['POST'])
@tokens.token_required
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

@payments_bp.route("/payments/<id>", methods=['DELETE'])
@tokens.admin_required
def delete_payment(id):
    payment = Payments.query.get_or_404(id)
    user = Users.query.get(payment.userid)
    user.balance = user.balance - payment.amount
    db.session.delete(payment)
    db.session.commit()
    return f'"id":{payment.id},"result":"deleted"'
