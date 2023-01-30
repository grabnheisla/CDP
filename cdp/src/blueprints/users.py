from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from extensions.tokens import tokens
from datetime import datetime
from main import db
import jwt, os
users_bp = Blueprint('users_bp',__name__)
secret_key = os.environ.get('SECRET_KEY')

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=True)
    favorite = db.Column(db.Boolean, default=True)
    firstname = db.Column(db.String(200))
    lastname = db.Column(db.String(200))
    falseLogonCount = db.Column(db.Integer, nullable=False, default=0)
    password = db.Column(db.String(200))
    secretkey = db.Column(db.String(200))
    authmethod = db.Column(db.Integer,nullable=False, default=0)
    username = db.Column(db.String(200),unique=True,nullable=False)
    displayname = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200))
    balance = db.Column(db.Integer, default=0)
    admin = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    def __repr__(self):
        return f'{{"id": {self.id},"username":{self.username}}}'
    def __str__(self):
        return "{{'id':{self.id},'active':{self.active},'favorite':{self.favorite},'firstname':{self.firstname},'lastname':{self.lastname},'username':{self.username},'displayname':{self.displayname},'email':{self.email},'balance':{self.balance},'created_on':{self.created_on},'last_login':{self.last_login}, 'falseLogonCount':{self.falseLogonCount}}}"
    def toJson(self):
        userJson = {'id': self.id, 'active':self.active,'favorite':self.favorite,'firstname':self.firstname,'lastname':self.lastname,'username':self.username,'displayname':self.displayname,'email':self.email,'balance':self.balance,'created_on':self.created_on,'last_login':self.last_login, 'falseLogonCount':self.falseLogonCount, 'authmethod':self.authmethod }
        return userJson
    def toJsonDetailed(self):
        userJson = {'id': self.id, 'active':self.active,'admin':self.admin,'favorite':self.favorite,'firstname':self.firstname,'lastname':self.lastname,'username':self.username,'displayname':self.displayname,'email':self.email,'balance':self.balance,'created_on':self.created_on,'last_login':self.last_login, 'falseLogonCount':self.falseLogonCount, 'password':self.password, 'secretKey':self.secretkey,'authmethod':self.authmethod}
        return userJson
    def debit(id,amount):
        user = Users.query.get_or_404(id)
        user.balance = user.balance - amount
        return 0

@users_bp.route("/users")
def get_users():
    token = request.args.get('token')
    users = Users.query.filter(Users.favorite)
    if token:
        try:
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            if data['admin'] is True:
                users = Users.query.all()
        except:
            users = Users.query.filter(Users.favorite)       
    output = []
    for user in users:
        user_data = user.toJson()
        #user_data = {'id':user.id,'username':user.username,'displayname':user.displayname,'email':user.email,'balance':user.balance,'created_on':user.created_on,'last_logon':user.last_login}
        output.append(user_data)

    return output
@users_bp.route("/users/<id>",methods=['GET'])
@tokens.admin_required
def get_user(id):
    user = Users.query.get_or_404(id)
    return user.toJsonDetailed()

@users_bp.route("/users/<id>",methods=['PATCH'])
def update_user(id):
    user = Users.query.get_or_404(id)
    json = request.get_json()
    try: user.firstname = json['firstname']
    except: None
    try: user.lastname = json['lastname']
    except: None
    try: user.username = json['username']
    except: None
    try: user.favorite = bool(json['favorite'])
    except:None
    try: user.displayname = json['displayname']
    except:None
    try: user.active = bool(json['active'])
    except:None
    try: user.admin = bool(json['admin'])
    except:None
    try: user.email = json['email']
    except:None
    try: user.password = generate_password_hash(json['password'])
    except:None
    try: user.authmethod = json['authmethod']
    except:None

    db.session.commit()
    return user.toJsonDetailed()

@users_bp.route("/users", methods=['POST'])
@tokens.admin_required

def add_user():
    try: str_first = request.json['firstname'] 
    except: str_first = None
    try: str_last = request.json['lastname']
    except: str_last = None
    try: bool_fav = request.json['favorite']
    except: bool_fav = True
    try: str_mail = request.json['email']
    except: str_mail = None
    try: bool_admin = request.json['admin']
    except: bool_admin = False
    try: str_user = request.json['username']
    except: return {"response":"Username is required!"},400
    try: str_pass = generate_password_hash(request.json['password'])
    except: str_pass = generate_password_hash("")
    if Users.query.filter_by(username=str_user).first() is None:
        user = Users(username=str_user,displayname=request.json['displayname'],firstname=str_first, lastname=str_last, favorite=bool_fav,  email=str_mail,admin=bool_admin, password=str_pass, created_on=datetime.now())
        db.session.add(user)
        db.session.commit()
        return f'"id":"{user.id}"',201
    else:
        return {"response":"Username already taken!"},400

@users_bp.route("/users/<id>", methods=['DELETE'])
def delete_user(id):
    user = Users.query.get_or_404(id)
    if user is None:
        return {"response":"Not found"}
    db.session.delete(user)
    db.session.commit()
    return f'"id":{user.id},"result":"deleted"'


