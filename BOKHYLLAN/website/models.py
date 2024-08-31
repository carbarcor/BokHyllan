'''Denna fil innehåller strukturen för databasen.
"from . import db" - . leder programmets filer till databasens directory
(siffor)representerar max antal tecken som man kan skriva i fältet.'''
from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


# Definiera id för favoriter.
favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)

'''Klassen "rooms" representerar chattrummen där två användare möts.'''
class Rooms(db.Model):
    #identifiereingsnummer för rummet, unikt värde.
    id = Column(Integer, primary_key = True, autoincrement = True)
    #1_id för den första användaren i chattrummet.
    user_1_id = db.Column(db.String(150), ForeignKey('user.id'), nullable = False)
    ##2_id för den första användaren i chattrummet.
    user_2_id = db.Column(db.String(150), ForeignKey('user.id'), nullable = False)
    #koden till rummet. Unikt värde.
    room_code = db.Column(db.String(150), unique = True)
    #relation till den första användaren 1_id.
    user_1 = relationship("User", foreign_keys = [user_1_id])
    #relation till andra användaren 2_id.
    user_2 = relationship("User", foreign_keys = [user_2_id])
    

'''Databas för uppladdade böcker'''
class Book(db.Model):
    #skapar ett unikt identifieringsnummer för boken.
    id = db.Column(db.Integer, primary_key = True)
    # Titel på boken.
    title = db.Column(db.String(150))
    # Författare av boken.
    author = db.Column(db.String(150))
    # ISBN-nummer på boken.
    isbn = db.Column(db.String(150))
    # Bokens beskrivning.
    review = db.Column(db.String(30000))
    # Id för den användare som äger boken.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Bokens omslagsbild.
    cover_pic = db.Column(db.String())   

'''Databas för användare.
Primary key är det id som genereras automatiskt när en användare registrerar sig.'''
class User(db.Model, UserMixin):
    # Unikt identifieringsnummer för användaren.
    id = db.Column(db.Integer, primary_key = True)
    # E-postadress för användaren (unik).
    email = db.Column(db.String(150), unique = True)
    # Lösenord för användaren.
    password = db.Column(db.String(150))
    # Profilnamn(förnamn) för användaren.
    first_name = db.Column(db.String(150))
    # Relation till böcker som ägs av användaren.
    books = db.relationship('Book', backref = 'user')
    # Användarens biografi.
    bio = db.Column(db.String(30000))
    # Profilbild för användaren.
    profile_pic = db.Column(db.String())
    # Poäng för användaren (förvalt till 0).
    score = db.Column(db.Integer, default = 0)
    favorite_books = db.relationship('Book', secondary=favorites, backref=db.backref('favorited_by', lazy='dynamic'))
    reading_challenges = db.relationship('ReadingChallenge', back_populates='user')  # Ny rad för relationen
 
'''Databas för läsutmaningar.
Relation till Users för att kunna koppla användarens läsutmaningar med den inloggade användaren.'''
class ReadingChallenge(db.Model):
    __tablename__ = 'reading_challenges'
    # Primärnyckel för att identifiera varje läsutmaning unikt
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    goal = db.Column(db.String(200), nullable=False)
    target_number = db.Column(db.Integer, nullable=False)
    # progress(framsteg) för användaren (förvalt till 0).
    progress = db.Column(db.Integer, default=0)
    user = relationship('User', back_populates='reading_challenges')  # Relation till användare