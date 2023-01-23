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
    username = db.Column(db.String(200),unique=True,nullable=False)
    displayname = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200))
    balance = db.Column(db.Integer, default=0)
    created_on = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    def __repr__(self):
        return f'{{"id": {self.id},"username":{self.username}}}'
    def __str__(self):
        return f'{{"id":{self.id},"active":{self.active},"username":{self.username},"displayname":{self.displayname},"email":{self.email},"balance":{self.balance},"created_on":{self.created_on},"last_login":{self.last_login}}}'

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/users")
def get_users():
    users = Users.query.all()
    output = []
    for user in users:
        user_data = {'id':user.id,'username':user.username,'displayname':user.displayname,'email':user.email,'balance':user.balance,'created_on':user.created_on,'last_logon':user.last_login}
        output.append(user_data)

    return output
@app.route("/users/<id>")
def get_user(id):
    user = Users.query.get_or_404(id)
    return str(user)

@app.route("/users", methods=['POST'])
def add_user():
    try: 
        str_mail = request.json['email']
    except: 
        str_mail = None

    user = Users(username=request.json['username'],displayname=request.json['displayname'], email=str_mail, created_on=datetime.now())
    db.session.add(user)
    db.session.commit()
    return f'"id":"{user.id}"'

@app.route("/users/<id>", methods=['DELETE'])
def delete_user(id):
    user = Users.query.get(id)
    if user is None:
        return {"response":"Not found"}
    db.session.delete(user)
    db.session.commit()
    return f'"id":{user.id},"result":"deleted"'


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=port)
    