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
    return jsonify("Hello fellow PO's")

@routes.route("users", strict_slashes=False, methods=['GET'])
def get_all_users():
    return jsonify(User.query.all())

@routes.route("users/<user_id>", strict_slashes=False, methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    return jsonify(user), 200

@routes.route("users", strict_slashes=False, methods=['POST'])
def add_user():
    payload = request.get_json()
    try:
        if "email" not in payload :
            raise MissingFieldError("email")
        if "username" not in payload :
            raise MissingFieldError("username")
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
        if "content" not in payload :
           raise MissingFieldError("content")
    except KeyError as e:
        raise MissingFieldError(e.args[0])

    new_question = Question(content=payload["content"], chapter_id=payload["chapter_id"])
    try:
        new_question.save()
    except exc.IntegrityError as e:
        raise DuplicationError(e.args[0])

    return jsonify(new_question), 201

# Get all questions
@routes.route("questions", strict_slashes=False, methods=['GET'])
def get_all_questions():
    return jsonify(Question.query.all())

# Create a vote
@routes.route("votes", strict_slashes=False, methods=['POST'])
def add_vote():
    payload = request.get_json()

    try:
        if "question_id" not in payload :
            raise MissingFieldError("question_id")
        if "user_id" not in payload :
            raise MissingFieldError("user_id")
    except KeyError as e:
        raise MissingFieldError(e.args[0])

    question_id=payload["question_id"]
    user_id=payload["user_id"]
    print(question_id)
    print(user_id)

    try:
        new_vote = Vote(question_id=question_id, user_id=user_id)
    except KeyError as e:
        raise MissingFieldError(e.args[0])


    voted_question = Question.query.get(question_id)
    if voted_question is None:
        raise NotFound(question_id)
    voting_user = User.query.get(user_id)
    if voting_user is None:
        raise NotFound(user_id)

    try:
        voted_question.votes.append(new_vote)
        voted_question.save()
    except exc.IntegrityError as e:
        raise DuplicationError(e.args[0])

    voted_question = Question.query.get(question_id)

    return jsonify(voted_question), 201



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
