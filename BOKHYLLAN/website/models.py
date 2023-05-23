'''Denna fil innehåller strukturen för databasen.
"from . import db" - . leder programmets filer till databasens directory'''
from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

#declassromms representerar den rummen där två användare möts.
class Rooms(db.Model):
    #identifiereingsnummer för rummet, det är unik
    id = Column(Integer, primary_key=True, autoincrement=True)
    #1_id för den första användaren i rummet
    user_1_id = db.Column(db.String(150), ForeignKey('user.id'), nullable=False)
    ##2_id för den första användaren i rummet
    user_2_id = db.Column(db.String(150), ForeignKey('user.id'), nullable=False)
    #koden till rummet. unik
    room_code = db.Column(db.String(150), unique=True)
#relation till den första användaren 1_id
    user_1 = relationship("User", foreign_keys=[user_1_id])
#relation till andra användaren 2_id
    user_2 = relationship("User", foreign_keys=[user_2_id])
    

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