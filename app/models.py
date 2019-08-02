#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    job = db.Column(db.String(120), nullable=True)
    pets = db.relationship('Pet', backref='owner', lazy=True)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return '<User %r>' % self.username


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return '<Pet %r>' % self.pet_name

# Chapter class definition
class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)

# Question class definition
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=True)
    votes = db.Column(db.Integer, nullable=False, default=0)

# Add function
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

# Update function
    def update(self,payload):
        db.session.query(Question).filter(Question.id == self.id).update(payload)
        db.session.commit()
        return self

    def __repr__(self):
        return '<Question %r>' % self.id
