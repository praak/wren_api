from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from bson.json_util import dumps
import pymongo
from pymongo import MongoClient
import json
import datetime
import string
import requests
# https://pypi.python.org/pypi/noaaweather/0.1.0
from noaaweather import weather

connection = MongoClient('localhost:27017')
app = Flask(__name__)

@app.route('/test/', methods=['GET'])
def get_test():
  h = int(request.args.get('hour'))
  m = int(request.args.get('minute'))
  s = int(request.args.get('second'))
  db = connection.wrendb.testcollection

  sfWeather = weather.noaa()
  sfWeather.getByZip('45236')
  print sfWeather.precipitation.liquid.tomorrow.max.value
  print sfWeather.temperature.apparent.tomorrow.min.value
  print sfWeather.temperature.apparent.value

  return get(db, h, m, s), 200
   
@app.route('/', methods=['GET'])
def get_data():
  h = int(request.args.get('hour'))
  m = int(request.args.get('minute'))
  s = int(request.args.get('second'))
  db = connection.wrendb.sensorcollection
  return get(db, h, m, s), 200

## Handle GET requests
def get(db, h, m, s):
  now = datetime.datetime.now()
  past = now - datetime.timedelta(hours=h, minutes=m, seconds=s)
  spast = str(past.isoformat())

  results = list(db.find({'published_at' : {'$gte' : spast}}, {'_id' : 0}).sort('published_at', pymongo.DESCENDING))
  return jsonify(results)


@app.route('/test/', methods=['POST'])
def add_test():
  db = connection.wrendb.testcollection
  form = request.form
  return post(db, form), 200

@app.route('/', methods=['POST'])
def add_data():
  db = connection.wrendb.sensorcollection
  form = request.form
  return post(db, form), 200


## Handle POST requests
def post(db, form):
  data = form['data']
  jdata = json.loads(data)
  
  jstring = {'coreid' : form['coreid'], 'event' : form['event'], 'published_at' : form['published_at'], \
            'WallTemp' : jdata['WallTemp'], \
            'RemoteId1' : jdata['RemoteId1'], 'Temp1' : jdata['Temp1'], 'BattStatus1' : jdata['BattStatus1'], \
            'RemoteId2' : jdata['RemoteId2'], 'Temp2' : jdata['Temp2'], 'BattStatus2' : jdata['BattStatus2']} 

  db.insert_one(jstring)  
  return ' '

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
