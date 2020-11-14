import json

database = {}

def save():
    with open('db.json', 'w') as filehandler:
        json.dump(database, filehandler)

def load():
    global database
    with open('db.json', 'r') as filehandler:
        database = json.load(filehandler)

def get_database():
    global database
    return database

