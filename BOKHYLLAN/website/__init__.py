#detta är jätte viktigt for flask eftersom det genererar automatisk databasen, 
#den tillåter oss att skapa ett lösenord för att administrerat administratörsområdet
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager

#själva databasen
db = SQLAlchemy()
DB_NAME = "database.db"


"""
fungerar inte nu vet inte om vi behöver den
def create_img_dir(app):
    Newfolder='Img'
    if not path.exists('website/static' + Newfolder):
        os.makedirs(Newfolder)"""
    
#detta är flaskappen. detta är obligatorisk utan den funkar inte programmet.
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Tito'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    """importerar phytonkoden till programmet"""
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Book
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#den skapa filen fysiskt dvs:databasen
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
