from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Book
from . import db
from werkzeug.utils import secure_filename
import uuid as uuid
import os

'''Variabel för blueprint. Detta organiserar appen/programmet'''
views = Blueprint('views', __name__)


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
        title = request.form.get('title')
        author = request.form.get('author')
        isbn = request.form.get('isbn')
        review = request.form.get('review')
        new_book = Book(title=title,author=author, isbn=isbn, review=review, user_id=current_user.id)
        db.session.add(new_book)
        db.session.commit()
        flash('Boken har laddats upp!', category='success')
        return redirect(url_for('views.add_book'))
    
    return render_template('add_book.html', user=current_user, books=books )


'''Funktion för att ta bort en uppladdad bok'''
@views.route('/remove-book/<int:book_id>', methods=['POST'])
@login_required
def remove_book(book_id):
    book = Book.query.get(book_id)

    if book.user_id == current_user.id:
        db.session.delete(book)
        db.session.commit()
        flash('Boken har tagits bort!', category='success')
    else:
        flash('Du kan bara ta bort dina egna böcker!', category='error')
    return redirect(url_for('views.add_book'))


'''Funktion för att ladda upp bild (över bok eller biografi?)
Det är inte klart, saknas förstarka "security" som görs genom werkzeug'''

@views.route('/add-pic', methods=['GET', 'POST'])
@login_required
def add_pic():
    if request.method == "POST":
        if request.files:
            image = request.files['image']
            pic_name = secure_filename(image.filename)
            pic_file_name = str(uuid.uuid1()) + "_" + pic_name
            pic_user = User.query.filter_by(id=current_user.id).first()
            pic_user.profile_pic = pic_file_name
            """saver.save(os.path.join(views.config['UPLOAD_FOLDER'], pic_name))"""
            if image == None:
                flash('Bilden har inte sparat!', category='error')
                return redirect(url_for('views.home'))
            else:
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
            flash('Biografin har inte skapats!', category='error')
            return redirect(url_for('views.home'))
        else:
            db.session.commit()
            flash('Biografin har skapats!', category='success')
            return redirect(url_for('views.home'))

    return render_template("add_bio.html", user=current_user)


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