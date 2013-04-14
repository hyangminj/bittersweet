from pymongo import MongoClient
from flask import Flask, render_template
app = Flask(__name__)
db = MongoClient().test

@app.route('/')
def hello():
  return render_template('home.html')

@app.route('/tweets')
def tweets():
  data = db.lalasweet_bot.find()
  return render_template('tweets.html', data=data)

@app.route('/settings')
def settings():
  return render_template('settings.html')

@app.route('/logs')
def logs():
  return render_template('logs.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
