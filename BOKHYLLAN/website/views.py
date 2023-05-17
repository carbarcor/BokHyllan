"""
vi importera fråm flask de olika paket som redo finns för att kunna
byga olika funktioner i programmet
Blueprint hjälpa oss att dela projektet och sortera i olika files.
render_template för att flask kan använda sig av html, 
request hjälp oss att kuna använda POST-method och GET-method,
flash pop up meddelanderna, 
redirect och url_for de hänvisar oss till funktion eller path,
current_app användar vi för att konfigurerar själva appen
werkzeug.utils det hjälper till att säkra filer och kod
secure_filename files namn
uuid funktionene skapar ett unik namn för filen, blanda det och krypterar
datum samt tid för överlappande av filen
os en del av standarbiblioteket, låter användaren interagera med det inbyggda operativsystemet phyton körs på
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, session
from flask_login import login_required, current_user
from .models import User, Book
from . import db
from werkzeug.utils import secure_filename
import uuid as uuid
import os
import random

'''Variabel för blueprint. Detta organiserar appen/programmet'''
views = Blueprint('views', __name__)

@views.route('/book-file/<int:book_id>', methods=['GET'])
@login_required
def book_file(book_id):
    book = Book.query.get(book_id)
    user = User.query.filter_by(id=current_user.id).first()
    owner = Book.user_id

    return render_template('book_page.html', book=book, user = user, owner= owner)

"""denna funktion (sökfunktion) letar efter bok i db. Vi vålde denna funktion
för att det letar fram det mest liknande resultatet """
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


'''Funktion för användaren att lägga till en bok för utbyte.
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


'''Funktion för att ladda upp bild (över bok eller biografi?)
Det är inte klart, saknas förstarka "security" som görs genom werkzeug'''


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


#vi kommer att komenterar varje rad.
@views.route('/add-pic', methods=['GET', 'POST'])
@login_required
def add_pic():
    if request.method == "POST":
        if request.files:
            delete_old_pic()
            #den fisiska filen sparas i denna variabel.
            image = request.files['image']
            #i denna variable säkerställa filen. 
            pic_name = secure_filename(image.filename)
            #filen få en unik namn.
            pic_file_name = str(uuid.uuid1()) + "_" + pic_name
            #hämta current user och letar efter den i databasen.
            pic_user = User.query.filter_by(id=current_user.id).first()
            #denna är profil bild Kolumn i databasen.
            pic_user.profile_pic = pic_file_name
            # image refererat till image html om det är inte en request så vissar att det är en error.
            if 'image' not in request.files:
                flash('Bilden har inte sparat!', category='error')
                return redirect(url_for('views.add_pic'))
            #om user clicka på skicka utan att ladda upp en bildformat så vissar error.
            if pic_name == '':
                flash('Ingen fil har valts')
                return redirect(url_for('views.add_pic'))
            #kontrolerar filen, om filen är inte godkänns som vissar att det kan man inte göra
            if allowed_file(image.filename) == False:
                flash('filformat inte tillåtet!')
                return redirect(url_for('views.add_pic'))
            else:
                image and allowed_file(image.filename)
                #spara filden i mappen: static/images
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


@views.route('/policy')
@login_required
def policy():
    
    return render_template('policy.html', user=current_user)



"""Error 404. Funktion som skickar användare till error-sida 400 """
@views.app_errorhandler(404)
def page_not_found(e):
    quotes = ["Why, sometimes I've believed as many as six impossible things before breakfast.",
                "It's no use going back to yesterday, because I was a different person then.",
                "'Who in the world am I?' Ah, that's the great puzzle!",
                "'And what is the use of a book,' thought Alice, 'without pictures or conversation?'",
                "Off with their heads!"]
    quote = random.choice(quotes)
    return render_template('error_404.html', quote = quote), 404

"""Error 500. Funktion som skickar användare till error-sida 500"""
@views.app_errorhandler(500)
def page_not_found(e):
    quotes = ["Why, sometimes I've believed as many as six impossible things before breakfast.",
                "It's no use going back to yesterday, because I was a different person then.",
                "'Who in the world am I?' Ah, that's the great puzzle!",
                "'And what is the use of a book,' thought Alice, 'without pictures or conversation?'",
                "Off with their heads!"]
    quote = random.choice(quotes)
    return render_template('error_500.html', quote = quote), 500



"""@views.route('/delete-bio', methods=['POST'])
def delete_bio():
    bio = json.loads(request.data)
    bioId = bio['bioId']
    bio = Bio.query.get(bioId)
    if bio:
        if bio.user_id == current_user.id:
            db.session.delete(bio)
            db.session.commit()
            return jsonify({})"""