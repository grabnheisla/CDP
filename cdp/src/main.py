from flask import Flask, request, Blueprint
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

app = Flask(__name__)
cors = CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB')
migrate = Migrate()
db = SQLAlchemy(app)
migrate.init_app(app,db)

basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('DB') or 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

from blueprints.users import users_bp
from blueprints.payments import payments_bp
from blueprints.purchases import purchases_bp
from blueprints.products import products_bp
from blueprints.authentication import auth_bp


app.register_blueprint(users_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(products_bp)
app.register_blueprint(purchases_bp)
app.register_blueprint(auth_bp)
