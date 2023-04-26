#här är strukteren till själva database.
"""punkten ledar programnet filer databasen directory"""
from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

#detta är databasen för bocker
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    author = db.Column(db.String(150))
    isbn = db.Column(db.String(150))
    review = db.Column(db.String(30000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cover_pic = db.Column(db.String(30000))


#detta är databasen för user. där PK är id som genereras automatisk när user registrerar sig
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    books = db.relationship('Book')
    bio = db.Column(db.String(30000))
    profile_pic = db.Column(db.String(30000))