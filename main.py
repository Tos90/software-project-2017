from flask import Flask,render_template, redirect, url_for, session, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
import datetime
from time import gmtime, strftime


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
class GamesTable(db.Model):
    __tablename__="GamesTable"
    gameID=db.Column(db.Integer,db.ForeignKey('ActiveUsers.gameID'),primary_key=True,nullable=False,autoincrement=True)
    NumPlayers=db.Column(db.Integer, index=True, unique=False)
    activeUsers = db.relationship("ActiveUsers", backref="GamesTable")

    def __init__(self,NumPlayers):
        self.NumPlayers = NumPlayers
class ActiveUsers(db.Model):
    __tablename__="ActiveUsers"
    ID=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(30), index=True, unique=True)
    gameID=db.Column(db.Integer,nullable=False)

    def __init__(self):
        self.username = current_user.username
class Seat(db.Model):
	__tablename__="SeatsTable"
	seat_id = db.Column("ID",db.Integer,primary_key=True)
	username = db.Column("username",db.String(255))
	gameID = db.Column("GameID",db.Integer)
	seatNum = db.Column("SeatNum",db.Integer)
	timestamp = db.Column("timestamp",db.DateTime,default=datetime.datetime.utcnow)

	def __init__(self,username,gameID,seatNum):
		self.username = username
		self.gameID = gameID
		self.seatNum = seatNum
class LoginForm(FlaskForm): #define login form for bootstrap
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
@app.route('/hello')
def hello_world():
  return render_template('index.html')

@app.route('/')
def hello():
	return "hi there"
if __name__ == '__main__':
  app.run()
