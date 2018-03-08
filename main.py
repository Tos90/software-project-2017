from flask import Flask,render_template, redirect, url_for, session, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField


app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'hi'

@app.route('/hello')
def hello():
	return "hi there"
if __name__ == '__main__':
  app.run()
