#!/usr/bin/python
# coding=utf-8

class BadRequest(Exception):

    def __init__(self):
        self.message = "Bad request"

class DuplicationError(BadRequest):

    def __init__(self, field):
        self.message = "Field {wrong} already exist".format(wrong=field)

class MissingFieldError(BadRequest):

    def __init__(self,field):
        self.message = "Field {field} is required".format(field=field)

class NotFound(Exception):

    def __init__(self, resource):
        self.message = "Could not find the resource: {resource}".format(resource=resource)
