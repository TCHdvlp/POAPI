#!/usr/bin/python
# coding=utf-8

from flask.json import JSONEncoder
from .models import User, Pet, Question, Vote
from .exceptions import *

class PoapiJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return{
                'id':obj.id,
                'username':obj.username,
                'email':obj.email,
                'job':obj.job
            }

        if isinstance(obj, Exception):
            return {
                'message':obj.message
            }

        if isinstance(obj, Question):
            return {
                'id':obj.id,
                'content':obj.content,
                'chapter_id':obj.chapter_id,
                'votes': obj.votes
            }

        if isinstance(obj, Vote):
            return {
                'question_id':obj.question_id,
                'user_id':obj.user_id
            }

        return super(PoapiJSONEncoder, self).default(obj)
