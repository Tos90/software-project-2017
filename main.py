from flask import Flask,render_template, redirect, url_for, session, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql2223630:aC2%mZ9%@sql2.freemysqlhosting.net/sql2223630'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    __tablename__ = "registration_details"
    user_id = db.Column('ID',db.Integer , primary_key=True)
    username = db.Column('username', db.String(255))
    password = db.Column('password', db.String(255))
    email = db.Column('email', db.String(255))
    balance = db.Column('balance', db.Integer)

    def __init__(self, user_id, username ,password, email, balance):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.balance = balance

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.user_id)

    def __repr__(self):
        return '<User %r>' % (self.username)

@app.route('/hello')
def hello_world():
  return render_template('index.html')

@app.route('/')
def hello():
	return "hi there"
if __name__ == '__main__':
  app.run()
