from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import pymongo
import re
import gallery
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

# cloudinary image upload
CLOUD_NAME = os.environ.get('CLOUD_NAME')
UPLOAD_PRESET = os.environ.get('UPLOAD_PRESET')


@app.route('/')
def home():
    return "It's working!"

# route to show all recipes

# @app.route('/recipe')
# def show_recipes():
#     all_recipes = db.recipes.find()
#     print(all_recipes)
#     return render_template('all_recipes.template.html', all_recipes=all_recipes)

@app.route('/recipe', methods=['GET', 'POST'])
def show_recipes():
    if request.method == 'GET':
        all_recipes = db.recipes.find()
        print(all_recipes)
        return render_template('all_recipes.template.html', all_recipes=all_recipes)
    
    if request.method == 'POST':
        name = request.form.get('name')
        cuisine = request.form.getlist('cuisine')
        meal_type = request.form.get('meal_type')

        critera = {}

        if name:
            critera['name'] = {
                '$regex': name,
                '$options': 'i'  # i means 'case-insensitive'
            }

        if len(cuisine) > 0 and cuisine[0] != "":
            critera['cuisine'] = {
                '$in': cuisine
            }

        print(cuisine)

        if meal_type:
            critera['meal_type'] = {
                '$regex': meal_type,
                '$options': 'i'  # i means 'case-insensitive'
            }
        print(meal_type)
        print(critera)

        results = db.recipes.find(critera)
        return render_template('display_results.template.html',
                            all_recipes=results,
                            name=name)


# for testing cloudinary image upload widget
@app.route('/recipes/uploadimage')
def upload_image():
    return render_template('uploadimage.template.html', cloudName=CLOUD_NAME, uploadPreset=UPLOAD_PRESET)

# route to create recipe
@app.route('/recipes/create')
def show_create_recipes():
    return render_template('create_recipe.template.html', cloudName=CLOUD_NAME, uploadPreset=UPLOAD_PRESET)

# route to process recipe form  
@app.route('/recipes/create', methods=['POST'])
def process_create_recipes():
    name = request.form.get('recipe_name')
    description = request.form.get('description')
    servings = request.form.get('servings')
    ingredients = request.form.get('ingredients')
    directions = request.form.get('directions')
    cuisine = request.form.getlist('cuisine')
    meal_type = request.form.get('meal_type')
    media = request.form.get('media')
    image = request.form.get('uploaded_file_url')
    contributor = request.form.get('contributor')
    email = request.form.get('email')

    if len(name) == 0:
        flash("Name cannot be empty", "error")
        return render_template('create_recipe.template.html')

    pre_ingredients = ingredients.split(';')
    new_ingredients = []
    for p in pre_ingredients:
        if re.search('[a-zA-Z]', p):
            new_ingredients.append(p)

    print(new_ingredients)

    pre_directions = directions.split(';')
    new_directions = []
    for d in pre_directions:
        if re.search('[a-zA-Z]', d):
            new_directions.append(d)

    print(new_directions)

    new_record = {
        'name': name,
        'description': description,
        'servings': servings,
        'ingredients': new_ingredients,
        'directions': new_directions,
        'cuisine': cuisine,
        'meal_type': meal_type,
        'media': media,
        'image': image,
        'contributor': contributor,
        'email': email
    }

    result = db.recipes.insert_one(new_record)
    print(result.inserted_id)
    flash("New recipe created successfully", "success")
    return redirect(url_for('show_recipe', recipe_id=result.inserted_id))

# viewing 1 recipe


@ app.route('/recipes/view/<recipe_id>')
def show_recipe(recipe_id):
    recipe = db.recipes.find_one({
        '_id': ObjectId(recipe_id)
    })
    return render_template('one_recipe.template.html', recipe=recipe)


@app.route('/recipes/edit/<recipe_id>')
def edit_recipe(recipe_id):
    recipe = db.recipes.find_one({
        '_id': ObjectId(recipe_id)
    })
    return render_template('edit_recipe.template.html', recipe=recipe, cloudName=CLOUD_NAME, uploadPreset=UPLOAD_PRESET)


@app.route('/recipes/edit/<recipe_id>', methods=['POST'])
def process_edit_recipes(recipe_id):
    name = request.form.get('recipe_name')
    description = request.form.get('description')
    servings = request.form.get('servings')
    ingredients = request.form.get('ingredients')
    directions = request.form.get('directions')
    cuisine = request.form.getlist('cuisine')
    meal_type = request.form.get('meal_type')
    media = request.form.get('media')
    image = request.form.get('uploaded_file_url')
    contributor = request.form.get('contributor')
    email = request.form.get('email')

    pre_ingredients = ingredients.split(';')
    new_ingredients = []
    for p in pre_ingredients:
        if re.search('[a-zA-Z]', p):
            new_ingredients.append(p)

    print(new_ingredients)

    pre_directions = directions.split(';')
    new_directions = []
    for d in pre_directions:
        if re.search('[a-zA-Z]', d):
            new_directions.append(d)

    print(new_directions)

    db.recipes.update_one({
        "_id": ObjectId(recipe_id)
    }, {
        '$set': {
            'name': name,
            'description': description,
            'servings': servings,
            'ingredients': new_ingredients,
            'directions': new_directions,
            'cuisine': cuisine,
            'meal_type': meal_type,
            'media': media,
            'image': image,
            'contributor': contributor,
            'email': email
        }
    })

    flash("Recipe edited successfully", "success")
    return redirect(url_for('show_recipe', recipe_id=recipe_id))


@app.route('/recipes/search')
def show_search_form():
    return render_template('search.template.html')


@app.route('/recipes/search', methods=['POST'])
def process_search_form():
    name = request.form.get('name')
    cuisine = request.form.getlist('cuisine')
    meal_type = request.form.get('meal_type')

    critera = {}

    if name:
        critera['name'] = {
            '$regex': name,
            '$options': 'i'  # i means 'case-insensitive'
        }

    if len(cuisine) > 0 and cuisine[0] != "":
        critera['cuisine'] = {
            '$in': cuisine
        }

    print(cuisine)

    if meal_type:
        critera['meal_type'] = {
            '$regex': meal_type,
            '$options': 'i'  # i means 'case-insensitive'
        }

    print(critera)

    results = db.recipes.find(critera)
    return render_template('display_results.template.html',
                           all_recipes=results,
                           name=name)


@app.route('/recipes/delete/<recipe_id>')
def show_confirm_delete(recipe_id):
    # should use find_one, expecting one result
    recipe_to_delete = db.recipes.find_one({
        '_id': ObjectId(recipe_id)
    })
    return render_template('show_confirm_delete.template.html',
                           recipe=recipe_to_delete)


@app.route('/recipes/delete/<recipe_id>', methods=["POST"])
def confirm_delete(recipe_id):
    email = request.form.get('email')

    recipe_to_delete = db.recipes.find_one({
        '_id': ObjectId(recipe_id)
    })

    print(recipe_to_delete)
    print(recipe_to_delete['email'])

    if email == recipe_to_delete['email']:
        db.recipes.remove({
            "_id": ObjectId(recipe_id)
        })
        flash("Recipe is successfully deleted", "success")

    else:
        flash("You have typed the incorrect contributor email! Recipe cannot be deleted", "error")

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
