from flask import Flask, render_template, request
from datetime import datetime, timedelta
from functools import wraps
from main import app
import jwt
import os

secret_key = os.environ.get('SECRET_KEY')

class tokens:
    
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.args.get('token')
            if not token:
                return {"response":"Token is missing!"},403
            try:
                data = jwt.decode(token, secret_key, algorithms=['HS256'])
            except:
                return {"response":"Token is invalid!"},403
            
            return f(*args, **kwargs)
        return decorated

    def admin_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.args.get('token')
            if not token:
                return {"response":"Token is missing!"},403
            try:
                data = jwt.decode(token, secret_key, algorithms=['HS256'])
                if data['admin'] is not True:
                    return {"response":"User is not an Admin"},403
            except:
                    return {"response":"Token is invalid!"},403
            
            return f(*args, **kwargs)
        return decorated
