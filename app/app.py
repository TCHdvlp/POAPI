#!/usr/bin/python
# coding=utf-8

from flask import Flask, jsonify, url_for
from flask_cors import CORS
from .models import db, User, Chapter, Vote
from .json_encoder import PoapiJSONEncoder
from .routes import routes
from .exceptions import *


# ********************** CONFIG **********************

# create the application
app = Flask("poapi")

# CORS handling
CORS(app, resources={r"/*": {"origins": "*"}})

# custom jsonEncoder
app.json_encoder = PoapiJSONEncoder

# database connexion
database_url = 'sqlite://'  # this is a local in-memory database for testing purpose only
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

# init database model
db.app = app
db.init_app(app)
db.create_all()


# ************** MODELS INITIALIZATION ***************

admin = User(username='admin', email='admin@example.com')
guest = User(username='guest', email='guest@example.com', job='consultant')
chapter = Chapter()

db.session.add(admin)
db.session.add(guest)
db.session.add(chapter)
# this line should be the last in order to insert all tuples
db.session.commit()


# ********************* ROUTES *********************

app.register_blueprint(routes, url_prefix='/poapi/')

# ************** HANDLING EXCEPTIONS ***************

@app.errorhandler(BadRequest)
def badrequesterrorhandler(error):
    print(error)
    return jsonify(error), 400

# Not Found error handler
@app.errorhandler(NotFound)
def notfounderrorhandler(error):
    print(error)
    return jsonify(error), 404
