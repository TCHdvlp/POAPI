#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from .models import Pet, User, Question, Vote
from sqlalchemy import exc
from .exceptions import *

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

    try:
        if not payload["email"] : raise MissingFieldError("email")
        if not payload["username"] : raise MissingFieldError("username")
    except KeyError as e:
        raise MissingFieldError(e.args[0])

    new_user = User(username = payload["username"], email = payload["email"], job = payload["job"])

    try :
        new_user.save()
    except exc.IntegrityError as e:
        raise DuplicationError(e.args[0])

    return jsonify(new_user), 201

# Create new question
@routes.route("questions", strict_slashes=False, methods=['POST'])
def add_question():
    payload = request.get_json()

    try:
        if not payload["content"] : raise MissingFieldError("content")
    except KeyError as e:
        raise MissingFieldError(e.args[0])

    try:
        new_question = Question(content=payload["content"], chapter_id=payload["chapter_id"])
    except KeyError as e:
        raise MissingFieldError(e.args[0])

    new_question.save()

    return jsonify(new_question), 201

# Retrieve all questions
@routes.route("questions", strict_slashes=False, methods=['GET'])
def get_all_questions():
    questions=Question.query.all()
    print("MON PRINT POUR DEBUG", questions)
    return jsonify(questions)

# Create a vote
@routes.route("votes", strict_slashes=False, methods=['POST'])
def add_vote():
    payload = request.get_json()

    try:
        if not payload["question_id"] : raise MissingFieldError("question_id")
        if not payload["user_id"] : raise MissingFieldError("user_id")
    except KeyError as e:
        raise MissingFieldError(e.args[0])

    try:
        new_vote = Vote(question_id=payload["question_id"], user_id=payload["user_id"])
    except KeyError as e:
        raise MissingFieldError(e.args[0])

        try :
            new_vote.save()
        except exc.IntegrityError as e:
            raise DuplicationError(e.args[0])

    return jsonify(new_vote), 201



# Update question
# @routes.route("questions/<question_id>", strict_slashes=False, methods=['PUT'])
# def update_question(question_id):
#     payload = request.get_json()
#
#     question = Question.query.filter_by(id=question_id).first()
#
#     try:
#         updated_question = question.update(payload)
#     except AttributeError as e:
#         raise NotFound("question {id}".format(id=question_id))
#
#     return jsonify(updated_question), 200
