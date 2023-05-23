'''Denna fil innehåller strukturen för databasen.
"from . import db" - . leder programmets filer till databasens directory
(siffor)representerar max antal tecken som man kan skriva'''
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
    #skapa en unik identifieringsnummer för boken.
    id = db.Column(db.Integer, primary_key=True)
    # Titel på boken.
    title = db.Column(db.String(150))
    # Författare till boken.
    author = db.Column(db.String(150))
    # ISBN-nummer för boken.
    isbn = db.Column(db.String(150))
    # Bokens recension, max 300000
    review = db.Column(db.String(30000))
    #id för den användaren som äger boken.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # bokens coversbild.
    cover_pic = db.Column(db.String())


'''Databasen för användare.
Primary key är id som genereras automatisk när en användare registrerar sig'''
class User(db.Model, UserMixin):
    # Unikt identifieringsnummer för användaren.
    id = db.Column(db.Integer, primary_key=True)
    # E-postadress för användaren (unik).
    email = db.Column(db.String(150), unique=True)
    # Lösenord för användaren.
    password = db.Column(db.String(150))
    # Förnamn för användaren.
    first_name = db.Column(db.String(150))
    # Relation till böcker som ägs av användaren.
    books = db.relationship('Book', backref='user')
    # Användarens biografi.
    bio = db.Column(db.String(30000))
    # Profilbild för användaren.
    profile_pic = db.Column(db.String())
    # Poäng för användaren (förvalt till 0).
    score = db.Column(db.Integer, default=0)