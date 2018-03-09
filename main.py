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
class RegisterForm(FlaskForm): #define registration form for bootstrap
    email = StringField('email', validators=[InputRequired(), Length(max=50), Email("This field requires a valid email address")])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
@app.route('/login', methods=['GET', 'POST']) #login page
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    username = form.username.data
    password = form.password.data
    registered_user = User.query.filter_by(username=username,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    session['username'] = username
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('lobby'))
@app.route('/waiting', methods=['GET', 'POST'])
@login_required
def waiting(): 
    return render_template("waiting.html")
@app.route('/newhand',methods=['GET','POST'])
def newhand():
	hand_count = 0
	handScore = 0
	hand = ""
	playerName = session['username']
	whichGame = ActiveUsers.query.filter_by(username=playerName).first()
	gameID = whichGame.gameID
	global deck
	clear_deck = Deck.query.filter_by(gameID=gameID)
	db.session.delete(clear_deck)
	db.session.commit()
	
	while hand_count < 2:
		nextcard = str(deck[0])
		cardsplayed = Deck.query.filter_by(gameID=gameID).all()
		
		if nextcard not in cardsplayed:
			handScore += deck[0]._cardValue
			newcard = Deck(card=nextcard,gameID=gameID)
			db.session.add(newcard)
			db.session.commit()
			hand_count += 1
			deck.remove(deck[0])
			hand += "," + nextcard
		else:
			deck.remove(deck[0])

	#get the line of dealer
	dealer_go = Actions.query.filter_by(type="dealer",gameID=game.gameID)
	current_time = datetime.datetime.now().time()
	diff_time = dealer.timestamp - current_time
	if diff_time < 3000: #gamelength
		dealer = Dealer()
		dealer_go.hand = dealer._handlst
		dealer_go.handValue = dealer._handValue
		dealer._go.timestamp = datetime.datetime.now().time()
		db.session.commit()
	#check if time is more than gamelength older that current time
	#if it is deal away mad
	#other wise pass	
	updatePlayerHand = Actions(action_name=playerName,action_type="player",action_game=gameID,action_move="new_hand",action_hand=hand,action_value=handScore,action_stake=0)
	db.session.add(updatePlayerHand)
	db.session.commit()
	nextCard= json.dumps(deck[0])
	return (handScore)

@app.route('/hello')
def hello_world():
  return render_template('index.html')

@app.route('/')
def hello():
	return "hi there"
if __name__ == '__main__':
  app.run()
