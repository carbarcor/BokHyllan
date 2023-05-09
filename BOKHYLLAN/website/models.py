'''Denna fil innehåller strukturen för databasen.
"from . import db" - . leder programmets filer till databasens directory'''
from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

'''Databasen för uppladdade böcker'''
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    author = db.Column(db.String(150))
    isbn = db.Column(db.String(150))
    review = db.Column(db.String(30000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cover_pic = db.Column(db.String())


'''Databasen för användare.
Primary key är id som genereras automatisk när en användare registrerar sig'''
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    books = db.relationship('Book', backref='user')
    bio = db.Column(db.String(30000))
    profile_pic = db.Column(db.String())
    score = db.Column(db.Integer, default=0)