import json

from pymongo import MongoClient

from sets import HOST


params = {
	'host': HOST,
	'port': 27017,
}

try:
	with open('keys.json', 'r') as file:
		MONGO = json.loads(file.read())['mongo']

	params['username'] = MONGO['login']
	params['password'] = MONGO['password']
	params['authSource'] = 'admin'
	params['authMechanism'] = 'SCRAM-SHA-1'

except:
	MONGO = {
		'db': 'uple',
	}

db = MongoClient(**params)[MONGO['db']]