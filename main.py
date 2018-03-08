from flask import Flask,render_template, redirect, url_for, session, request, flash
app = Flask(__name__)

@app.route('/')
def hello_world():
  return render_template('index.html')

@app.route('/hello')
def hello():
	return "hi there"
if __name__ == '__main__':
  app.run()
