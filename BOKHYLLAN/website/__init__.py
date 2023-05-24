#detta är jätte viktigt for flask eftersom det genererar automatisk databasen, 
#den tillåter oss att skapa ett lösenord för att administrerat administratörsområdet
from flask import Flask, flash
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_socketio import join_room, leave_room, send, SocketIO

#själva databasen
# Skapar en SQLAlchemy-databasinstans.
db = SQLAlchemy()
# Namn på databasfilen.
DB_NAME = "database.db"
# Skapar en SocketIO-instans.
socketio = SocketIO()

def create_app():
    # Skapar en Flask-appinstans.
    app = Flask(__name__)
    # Konfigurerar en hemlig nyckel för sessionhantering.
    app.config['SECRET_KEY'] = 'Tito'
    # Konfigurerar URI för SQLite-databasen.
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Konfigurerar URI för SQLite-databasen.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Konfigurerar inställningar för meddelandeflashing.
    app.config['MESSAGE_FLASHING_OPTIONS'] = {'duration': 5}
     # Initierar SocketIO med Flask-appen.
    socketio.init_app(app)
    
#denna är adressen där bilden sparas.
    UPLOAD_FOLDER = './BOKHYLLAN/website/static/images'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # Initierar SQLAlchemy med Flask-appen.
    db.init_app(app)
    # Importerar phytonfilen och autentisering från moduler.
    from .views import views
    from .auth import auth
    # Registrerar blueprint för phytonfilen och autentisering.
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    # Importerar modeller.
    from .models import User, Book
    # Initierar SocketIO med Flask-appen.
    with app.app_context():
        socketio.init_app(app)
    # Skapar databastabellerna om de inte redan finns.
    with app.app_context():
        db.create_all()
    # Initierar LoginManager för hantering av användarautentisering.
    login_manager = LoginManager()
    # Ange inloggnings view för LoginManager, interfunktion.
    login_manager.login_view = 'auth.login'
    # Initierar LoginManager med Flask-appen, intern fuktion
    login_manager.init_app(app)
    # Ange meddelandet för inloggningskrav.
    login_manager.login_message = 'Du måste logga in för att komma åt din hemsida!'
    
    
    # Anpassad funktion för att ladda användaren med användar-ID.
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    # Returnerar den skapade appen.
    return app

#den skapa filen fysiskt dvs:databasen
def create_database(app):
    if not path.exists('website/static' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
