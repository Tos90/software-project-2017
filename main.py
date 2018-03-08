from flask import Flask,render_template, redirect, url_for, session, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_table import Table, Col, LinkCol
from sqlalchemy.ext.declarative import declarative_base
from time import gmtime, strftime
from dealer import Dealer
from deck import Deck
import datetime
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'hi'

@app.route('/hello')
def hello():
	return "hi there"
if __name__ == '__main__':
  app.run()
