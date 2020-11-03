from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import pymongo
# from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv

if os.path.exists("env.py"):
    import env

load_dotenv()

# declare the global variables to store the URL to the Mongo database
MONGO_URL = os.environ.get('MONGO_URL')
DB_NAME = "recipesbook"

# create the Mongo client
client = pymongo.MongoClient(MONGO_URL)
# as db variable is outside of every functions, it is a global variable
# we can use the db variable inside any functions
db = client[DB_NAME]

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

@app.route('/')
def home():
    return "It's working!"

# route to show all recipes
@app.route('/recipes')
def show_recipes():
    all_recipes = db.recipes.find()
    return render_template('all_recipes.template.html', all_recipes=all_recipes)



# "magic code" -- boilerplate
#if __name__ == '__main__':
    # app.run(host=os.environ.get('IP'),     #must give a host (IP address)
    #         port=int(os.environ.get('PORT')),   #networking clients access
    #         debug=True)
if __name__ == '__main__': 
    app.run(host="localhost",     #must give a host (IP address)
            port=8080,   #networking clients access
            debug=True)

