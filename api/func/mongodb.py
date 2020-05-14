import json

from pymongo import MongoClient

from sets import HOST


try:
	with open('keys.json', 'r') as file:
		MONGO = json.loads(file.read())['mongo']
except:
	MONGO = {
		'login': None,
		'password': None,
	}

db = MongoClient(
	host=HOST,
	port=27017,
	username=MONGO['login'],
	password=MONGO['password'],
	authSource='admin',
	authMechanism='SCRAM-SHA-1'
)[MONGO['db']]