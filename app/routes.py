#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from models import Pet, User
from sqlalchemy import exc
from exceptions import *

routes = Blueprint('routes', __name__)


# ********************** ROUTES **********************

@routes.route("hello", strict_slashes=False)
def say_hello():
    return jsonify("Hello little PO's")

@routes.route("users", strict_slashes=False, methods=['GET'])
def get_all_users():
    return jsonify(User.query.all())

@routes.route("users", strict_slashes=False, methods=['POST'])
def add_user():
    payload = request.get_json()
    if not payload["email"] : raise MissingFieldError("email")
    if not payload["username"] : raise MissingFieldError("username")

    new_user = User(username = payload["username"], email = payload["email"], job = payload["job"])


    try :
        new_user.save()
    except exc.IntegrityError as e:
        raise DuplicationError(e.args[0])
    except KeyError as e:
        raise MissingFieldError(e.args[0])

    return jsonify(new_user), 201