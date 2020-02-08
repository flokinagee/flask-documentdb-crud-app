import os
import sys
import pymongo
from pymongo.errors import *

def get():
	url = os.environ['username'] + ":" + os.environ['password'] + "@" + os.environ['cluster_endpoint'] + ":" + os.environ['port'] + "/?replicaSet=rs0&readPreference=secondaryPreferred"
	try:
		client = pymongo.MongoClient('mongodb://localhost:27017/')
	except Exception as e:
		raise e
	else:
		return client

def close(client):
	##Close the connection
	return client.close()
