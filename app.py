from flask import Flask, render_template, request, redirect, url_for
import os


app = Flask(__name__)





@app.route('/')
@app.route('/home')
def home():
    return "It's working!"


# "magic code" -- boilerplate
#if __name__ == '__main__':
    # app.run(host=os.environ.get('IP'),     #must give a host (IP address)
    #         port=int(os.environ.get('PORT')),   #networking clients access
    #         debug=True)
if __name__ == '__main__': 
    app.run(host="localhost",     #must give a host (IP address)
            port=8080,   #networking clients access
            debug=True)

