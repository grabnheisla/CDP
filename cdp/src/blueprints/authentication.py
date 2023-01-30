from flask import Blueprint, request
from extensions.tokens import tokens
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

import pyotp
import time
import jwt
import json
import os

from main import db
from blueprints.users import Users

auth_bp = Blueprint('auth_bp',__name__)

secret_key = os.environ.get('SECRET_KEY')

@auth_bp.route("/login",methods=['POST'])
def login():
    info = json.loads(request.data)

    try:
        if os.getenv('AdminToken') != "":
            if info['token'] == os.getenv('AdminToken'):
                expTime = datetime.utcnow() + timedelta(minutes=30)
                token = jwt.encode({"uid": 0, "user": "MasterRoot", "admin":True,"exp":expTime}, secret_key)
                return {"token":token}
    except: os.environ['AdminToken'] = ""
    username = info.get('username','guest')
    password = info.get('password','')
    totp = info.get('totp','')
     
    user = Users.query.filter_by(username=username, active=True).first()
    if user is None:
        return {"response": "User not found or not active"},404
    
    if user.authmethod <= 1: # Normal 0Pin/1Password Auth
        if check_password_hash(user.password,password):
            expTime = datetime.utcnow() + timedelta(minutes=30)
            # return {"token_payload":{"uid": str(user.id), "user": user.username, "admin":str(user.admin),"exp":expTime}}
            token = jwt.encode({"uid": user.id, "user": user.username,"displayname":user.displayname, "admin":user.admin,"exp":expTime}, secret_key)
            return {"token":token}
        else:
            return {"response":"Username or Password wrong!"},401
    elif user.authmethod == 2: # 2FA Auth
        totpCheck = pyotp.TOTP(user.secretkey)
        if check_password_hash(user.password,password) and totpCheck.verify(totp,valid_window=2):
            expTime = datetime.utcnow() + timedelta(minutes=30)
            token = jwt.encode({"uid": user.id, "user": user.username,"displayname":user.displayname, "admin":user.admin,"exp":expTime}, secret_key)
            return {"token":token}
        else:
            return {"response":"Username, Password or TOTP wrong"},401
    elif user.authmethod == 3: # Only TOTP
        totpCheck = pyotp.TOTP(user.secretkey)
        if totpCheck.verify(otp=str(totp),valid_window=2):
            expTime = datetime.utcnow() + timedelta(minutes=30)
            token = jwt.encode({"uid": user.id, "user": user.username,"displayname":user.displayname, "admin":user.admin,"exp":expTime}, secret_key)
            return {"token":token}
        else:
            return {"response":"TOTP wrong"},403
    else:
        return {"response":"Authentication not successfull!"},401
    

@auth_bp.route("/users/gentotp",methods=['GET'])
def generate_totp():
    token = request.args.get('token')
    if not token:
        return {"response":"Token missing"},400
    try:
        data = jwt.decode(token, secret_key,algorithms=['HS256'])
    except: return {"response":"Token invalid"},400
    secKey = pyotp.random_base32()
    user = Users.query.get_or_404(data['uid'])
    user.secretkey = secKey
    db.session.commit()
    qrcodeData = "otpauth://totp/" + user.displayname + "?secret=" + secKey + "&issuer=CDP"
    return {"secretkey": secKey,"qrcodeData":qrcodeData}
