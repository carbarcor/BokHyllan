"""
Vi har importerat olika paket från flask som redan finns redo för att kunna
bygga de olika funktionena i programmet
Blueprint hjälper oss att dela projektet och sortera i olika files.
Render_template används för att flask ska kunna använda sig av html, 
Request hjälper oss för att kunna använda POST-method och GET-method,
Flash pop up meddelanderna. 
Redirect och url_for hänvisar oss till funktion eller path.
Current_app använder vi för att konfigurera själva appen.
werkzeug.utils hjälper till att säkra alla filer och kod.
secure_filename files namn.
uuid funktionene skapar ett unik namn för filen, blandar det och krypterar
datum samt tid för överlappande av filen.
os är en del av standarbiblioteket, låter användaren interagera med det inbyggda operativsystemet phyton körs på
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, abort, session
from flask_login import login_required, current_user
from .models import User, Book, Rooms
from . import db
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, send, join_room, leave_room
from string import ascii_uppercase
import uuid as uuid
import os
import random
import json


'''Variabel för blueprint. Detta organiserar appen/programmet'''
views = Blueprint('views', __name__)
rooms = {} 
socketio = SocketIO()

@views.route('/edit-book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get(book_id)
    if request.method == 'POST':        
        new_title = request.form.get('new_title')
        new_author = request.form.get('new_author')
        new_isbn = request.form.get('new_isbn')
        new_review = request.form.get('new_review')
        book.title = new_title
        book.author = new_author
        book.isbn = new_isbn
        book.review = new_review
        db.session.commit()
        flash('Boken har uppdaterats!', category='success')
        return redirect(url_for('views.home'))
    
    return render_template("edit_book.html",user = current_user, book = book)


def generate_room(length):
    while True:
        room_code = ''.join(random.choice(ascii_uppercase) for _ in range(length))
        existing_room = Rooms.query.filter_by(room_code=room_code).first()

        if not existing_room:
            existing_room = Rooms()
            existing_room.room_code = room_code
            db.session.commit()
            break

    return room_code


@views.route("/chat/<int:owner_id>", methods= ['POST'])
@login_required
def chat(owner_id):
        session.clear()
        if request.method == "POST": 
            book_owner_id = owner_id
            user_1 = User.query.get(current_user.id)
            user_1_name = user_1.first_name
            user_1_id = user_1.id
            user_2 = User.query.get(book_owner_id)
            user_2_name = user_2.first_name
            user_2_id = user_2.id
            email = user_2.email
            
            existing_room = Rooms.query.filter_by(user_1_id=user_1_id, user_2_id=user_2_id).first()

            if existing_room:
                return render_template("chat_room.html", 
                               user_1 = user_1_name, 
                               user_2 = user_2_name,
                               email = email, 
                               user = current_user, 
                               room_code = existing_room.room_code)
            else:
                new_room_code = generate_room(6)
                new_chat = Rooms(user_1_id=user_1_id, user_2_id=user_2_id, room_code=new_room_code)
                db.session.add(new_chat)
                db.session.commit()

            room_data = {"members": 0, "messages": []}
            room_json = json.dumps(room_data)

            session["room"] = room_json
            session["name"] = user_1_name
        
        return render_template("chat_room.html", 
                               user_1 = user_1_name, 
                               user_2 = user_2_name,
                               email = email,
                               user = current_user, 
                               room_code = new_room_code)


@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")


@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    print(f"{name} joined room {room}")


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")


@views.route('/book-file/<int:book_id>', methods=['GET'])
@login_required
def book_file(book_id):
    book = Book.query.get(book_id)
    id_owner = book.user_id
    user = User.query.filter_by(id=current_user.id).first()
    owner = User.query.filter_by(id=id_owner).first()
    
    return render_template('book_page.html', book=book, user = user, owner= owner)


"""Denna funktion (sökfunktion) letar efter bok i db. Vi valde denna funktion
för att den letar fram det mest liknande resultatet till sökningen användaren gör. """
@views.route('/search', methods=["POST"])
def search():
    form = request.form.get('searched')
    books = Book.query.filter_by().all()
    if form:
            books_result = Book.query.filter(
            (Book.title.ilike(f'%{form}%')) |
            (Book.author.ilike(f'%{form}%')) |
            (Book.isbn.ilike(f'%{form}%'))
        ).all()
    else:
        books_result = []
    
    print(books_result)
    return render_template("search.html", user=current_user, searched = form, books =books , result= books_result)


'''Funktion för route till homepage'''
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    books = Book.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, books=books)


'''Funktion för visning av biblioteket av samtliga uppladdade böcker'''
@views.route('/all-books')
@login_required
def show_all_books():
    books = Book.query.all()
    return render_template('all_books.html', user=current_user, books=books )


'''Funktion för att användaren ska kunna lägga till en bok för utbyte.
Boken läggs in i databasen samt visas på home.html'''
@views.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    books = Book.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        user = User.query.filter_by(id=current_user.id).first()
        cover = request.files['cover']
        cover_name = secure_filename(cover.filename)
        cover_file_name = str(uuid.uuid1()) + "_" + cover_name        
        title = request.form.get('title')
        author = request.form.get('author')
        isbn = request.form.get('isbn')
        review = request.form.get('review')
        if 'cover' not in request.files:
            flash('Bilden har inte sparat!', category='error')
            return redirect(url_for('views.add_book'))
        if cover_name == '':
            flash('Ingen fil har valts')
            return redirect(url_for('views.add_book'))
        if allowed_file(cover.filename) == False:
            flash('filformat inte tillåtet!')
            return redirect(url_for('views.add_book'))
        else:
            cover and allowed_file(cover.filename)
            cover.save(os.path.join(current_app.config['UPLOAD_FOLDER'], cover_file_name))
            new_book = Book(title=title,author=author, isbn=isbn, review=review, user_id=current_user.id, cover_pic= cover_file_name )
            user.score = user.score + 1
            db.session.add(new_book)
            db.session.commit()
            flash('Boken har laddats upp!', category='success')
            return redirect(url_for('views.home'))
    
    return render_template('add_book.html', user=current_user, books=books )
    

'''Funktion för att ta bort en uppladdad bok'''
@views.route('/remove-book/<int:book_id>', methods=['POST'])
@login_required
def remove_book(book_id):
    book = Book.query.get(book_id)
    user = User.query.filter_by(id=current_user.id).first()

    if book.user_id == current_user.id:
        db.session.delete(book)
        user.score = user.score - 1
        db.session.commit()
        flash('Boken har tagits bort!', category='success')
    else:
        flash('Du kan bara ta bort dina egna böcker!', category='error')
    return redirect(url_for('views.add_book'))


'''Funktioner för att ladda upp profilbild'''
ALLOWED_EXTENSIONS = { 'jpg', 'jpeg','gif'} #denna är de filerna som är godkänns för att ladda upp.

#jämfora filensnamn med den typ av fil som är godkänn dvs jpg och jpeg. 
def allowed_file(pic_name):
    return '.' in pic_name and \
           pic_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#denna är för att ta bort profilbilden från användaren och ta bort automatisk den gammla. 
def delete_old_pic():
    user = User.query.filter_by(id=current_user.id).first()
    old_profile_pic = str(user.profile_pic)
    path = str('./BOKHYLLAN/website/static/images/'+ old_profile_pic)
    if user.profile_pic  == old_profile_pic and user.profile_pic != "":
        os.remove(path)


#vi kommer att kommentera varje rad:
@views.route('/add-pic', methods=['GET', 'POST'])
@login_required
def add_pic():
    if request.method == "POST":
        if request.files:
            delete_old_pic()
            #den fysiska filen sparas i denna variabel.
            image = request.files['image']
            #i denna variable säkerställs filen. 
            pic_name = secure_filename(image.filename)
            #filen får en unik namn.
            pic_file_name = str(uuid.uuid1()) + "_" + pic_name
            #hämta current user och letar efter den i databasen.
            pic_user = User.query.filter_by(id=current_user.id).first()
            #denna är profil bild Kolumn i databasen.
            pic_user.profile_pic = pic_file_name
            # image refererat till image html om det är inte en request så visas error.
            if 'image' not in request.files:
                flash('Bilden har inte sparat!', category='error')
                return redirect(url_for('views.add_pic'))
            #om user klickar på skicka utan att ladda upp en bildformat så visas error.
            if pic_name == '':
                flash('Ingen fil har valts')
                return redirect(url_for('views.add_pic'))
            #kontrollerar filen, om filen är inte godkänns så visas det att det inte går
            if allowed_file(image.filename) == False:
                flash('filformat inte tillåtet!')
                return redirect(url_for('views.add_pic'))
            else:
                image and allowed_file(image.filename)
                #spara filen i mappen: static/images
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], pic_file_name))
                #bifoga filens namn i databasen
                db.session.commit()
                flash('Bilden har sparat!', category='success')
                return redirect(url_for('views.home'))

    return render_template('add_pic.html', user=current_user)


'''Funktion för att ladda upp användarens biografi'''
@views.route('/add-bio', methods=['GET', 'POST'])
@login_required
def add_bio():
    if request.method == 'POST':
        new_bio = request.form.get('bio')
        bio_user = User.query.filter_by(id=current_user.id).first()
        bio_user.bio = new_bio
        if new_bio == "":
            flash('Biografin kunde inte skapas, försök igen.', category='error')
            return redirect(url_for('views.home'))
        else:
            db.session.commit()
            flash('Biografin har skapats!', category='success')
            return redirect(url_for('views.home'))

    return render_template("add_bio.html", user=current_user)


'''Funktion för visning av sida för användarens uppladdade böcker'''
@views.route('/user-books')
@login_required
def user_books():
    books = Book.query.filter_by(user_id=current_user.id).all()
    return render_template('user_books.html', user=current_user, books=books)


'''Funktion för visning av sida för användarvillkor'''
@views.route('/policy')
@login_required
def policy():
    return render_template('policy.html', user=current_user)


'''Funktion som gör att en slumpmässig bok framvisas till användaren'''
@views.route('/random-book')
@login_required
def random_book():
    books = Book.query.filter(Book.user_id != current_user.id).all()
    if not books:
        flash('No books available.', category='error')
        return redirect(url_for('views.home'))

    random_book = random.choice(books)
    cover_pic_path = 'images/' + random_book.cover_pic  # Modify the path here

    book_data = {
        'title': random_book.title,
        'author': random_book.author,
        'cover_pic': cover_pic_path
    }
    return render_template('random_book.html', user=current_user, book=book_data)


"""Error 404. Funktion som skickar användare till error-sida 404 (client-error). Visar ett slumpat citat av 5 st """
@views.app_errorhandler(404)
def page_not_found(e):
    quotes = ["Why, sometimes I've believed as many as six impossible things before breakfast.",
                "It's no use going back to yesterday, because I was a different person then.",
                "'Who in the world am I?' Ah, that's the great puzzle!",
                "'And what is the use of a book,' thought Alice, 'without pictures or conversation?'",
                "Off with their heads!"]
    quote = random.choice(quotes)
    return render_template('error_404.html', quote = quote , user=current_user), 404


"""Error 505. Funktion som skickar användare till error-sida 505 (server-error: användare hittas ej). Visar ett slumpat citat av 5st """
@views.app_errorhandler(505)
def page_not_found(e):
    quotes = ["Why, sometimes I've believed as many as six impossible things before breakfast.",
                "It's no use going back to yesterday, because I was a different person then.",
                "'Who in the world am I?' Ah, that's the great puzzle!",
                "'And what is the use of a book,' thought Alice, 'without pictures or conversation?'",
                "Off with their heads!"]
    quote = random.choice(quotes)
    return render_template('error_505.html', quote = quote, user=current_user), 505


"""Error 500. Funktion som skickar användare till error-sida 500 (server-error: internt fel på servern) Visar ett slumpat citat av 5st"""
@views.app_errorhandler(500)
def page_not_found(e):
    quotes = ["Why, sometimes I've believed as many as six impossible things before breakfast.",
                "It's no use going back to yesterday, because I was a different person then.",
                "'Who in the world am I?' Ah, that's the great puzzle!",
                "'And what is the use of a book,' thought Alice, 'without pictures or conversation?'",
                "Off with their heads!"]
    quote = random.choice(quotes)
    return render_template('error_500.html', quote = quote , user=current_user), 500