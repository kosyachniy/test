"""
Database
"""

# Libraries
## System
import json

## External
from pymongo import MongoClient


# Params
with open('sets.json', 'r') as file:
    sets = json.loads(file.read())['mongo']


# Global variables
if sets['login'] and sets['password']:
    db = MongoClient(
        host=sets['host'],
        port=27017,
        username=sets['login'],
        password=sets['password'],
        authSource='admin',
        authMechanism='SCRAM-SHA-1'
    )[sets['db']]
else:
    db = MongoClient(
        host=sets['host'],
        port=27017,
    )[sets['db']]
