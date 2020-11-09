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

# route to create recipe


@app.route('/recipe/create')
def show_create_recipes():
    return render_template('create_recipe.template.html')

# route to process recipe form


@app.route('/recipe/create', methods=['POST'])
def process_create_recipes():
    name = request.form.get('recipe_name')
    description = request.form.get('description')
    servings = request.form.get('servings')
    ingredients = request.form.get('ingredients')
    directions = request.form.get('directions')
    cuisine = request.form.get('cuisine')
    meal_type = request.form.get('meal_type')
    media = request.form.get('media')
    contributor = request.form.get('contributor')
    email = request.form.get('email')

    if len(name) == 0:
        flash("Name cannot be empty", "error")
        return render_template('create_recipe.template.html')

    new_record = {
        'name': name,
        'description': description,
        'servings': servings,
        'ingredients': ingredients,
        'directions': directions,
        'cuisine': cuisine,
        'meal_type': meal_type,
        'media': media,
        'contributor': contributor,
        'email': email
    }

    db.recipes.insert_one(new_record)
    flash("New recipe created successful", "success")
    return redirect(url_for('show_recipes'))


# "magic code" -- boilerplate
# if __name__ == '__main__':
    # app.run(host=os.environ.get('IP'),     #must give a host (IP address)
    #         port=int(os.environ.get('PORT')),   #networking clients access
    #         debug=True)
if __name__ == '__main__':
    app.run(host="localhost",  # must give a host (IP address)
            port=8080,  # networking clients access
            debug=True)
