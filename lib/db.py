import os
import sys
from bson.json_util import dumps
sys.path.insert(0, "/Users/mahaakutty/code_space/repos/flask-app/lib")
import connections

def openc():
	return connections.get()

def close(client):
	return connections.close(client)

def get_collection(client):
	##Specify the database to be used
	db = client.flaskapp
	##Specify the collection to be used
	return db.myTestCollection


def get_logins(client):
	db = client.flaskapp
	return db.myTestlogins

def user_login():
	client = openc()
	return get_logins(client)

def add_user(data):
	try:
		client = openc()
		result = get_logins(client).insert_one(data)
		close(client)
	except Exception as e:
		raise e
	else:
		return result

def update_user(data):
	try:
		client = openc()
		result = get_logins(client).update({"_id": data['_id']}, data)
		close(client)
	except Exception as e:
		raise e
	else:
		return result

def get_user(field, identifier):
	try:
		client = openc()
		data = get_logins(client).find_one({identifier: field})
		close(client)
	except Exception as e:
		raise e
	else:
		return data

def get_data():
	try:
		client = openc()
		data = get_collection(client).find()
		close(client)
	except Exception as e:
		raise e
	else:
		return data

def get_customer_list():
	customer_list = []
	for data in get_data():
		customer_list.append(data['_id'])
	return get_customer_list

def get_customer(customer_id):
	try:
		client = openc()
		data = get_collection(client).find_one({"_id": customer_id})
		close(client)
	except Exception as e:
		raise e
	else:
		return data

def update(data):
	try:
		client = openc()
		result = get_collection(client).update({"_id": data['customer_id']}, data)
		close(client)
	except Exception as e:
		raise e
	else:
		return result


def add(data):
	try:
		client = openc()
		result = get_collection(client).insert_one(data)
		close(client)
	except Exception as e:
		raise e
	else:
		return result

def delete(customer_id):
	try:
		client = openc()
		result = get_collection(client).delete_one({"_id": customer_id})
		close(client)
	except Exception as e:
		raise e
	else:
		return result
