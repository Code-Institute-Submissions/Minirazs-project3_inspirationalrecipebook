from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
# from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


@app.route('/')
def home():
    return "It's working!"


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

