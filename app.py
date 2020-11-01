from flask import Flask, render_template, request, redirect, url_for
import os


app = Flask(__name__)

wsgi_app = app.wsgi_app

# "magic code" -- boilerplate
#if __name__ == '__main__':
    # app.run(host=os.environ.get('IP'),     #must give a host (IP address)
    #         port=int(os.environ.get('PORT')),   #networking clients access
    #         debug=True)
if __name__ == '__main__': 
  
    # run() method of Flask class runs the application  
    # on the local development server. 
    app.run()


@app.route('/')
@app.route('/home')
def home():
    return "It's working!"
