from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
  return render_template('blackjack.html')

@app.route('/hello')
def hello():
	return "hi there"
if __name__ == '__main__':
  app.run()
