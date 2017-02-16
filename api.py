from flask import Flask
from flask import jsonify
from flask import json
from flask import request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from pymongo import MongoClient
import datetime
import string

connection = MongoClient('localhost:27017')
app = Flask(__name__)

@app.route('/test/', methods=['GET'])
def get_test():
  db = connection.wrendb.testcollection
  return get(db), 200
   
@app.route('/', methods=['GET'])
def get_data():
  db = connection.wrendb.sensorcollection
  return get(db), 200

## Handle GET requests
def get(db):
  now = datetime.datetime.now()
  past = now - datetime.timedelta(minutes=1)
  spast = str(past.isoformat())

  results = list(db.find({'published_at' : {'$gte' : spast}}, {'_id' : 0}))
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
