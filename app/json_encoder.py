#!/usr/bin/python
# coding=utf-8

from flask.json import JSONEncoder
from models import User, Pet
from exceptions import *

class PoapiJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return{
                'id':obj.id,
                'username':obj.username,
                'email':obj.email,
                'job':obj.job
            }

        if isinstance(obj, BadRequest):
            return {
                'message':obj.message
            }

        return super(PoapiJSONEncoder, self).default(obj)
