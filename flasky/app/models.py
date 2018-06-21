#!/usr/bin/env python3
# coding=utf-8

from . import db


class Novel(db.Model):
    __tablename__ = 'novels'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    author = db.Column(db.String(64))
    chapters = db.relationship('Chapter', backref='novel', lazy='dynamic')

    def __repr__(self):
        return '<Novel %r>' % self.name


class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    chapter = db.Column(db.Integer)
    content = db.Column(db.Text)
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'))

    def __repr(self):
        return '<Chapter %r>' % self.title
