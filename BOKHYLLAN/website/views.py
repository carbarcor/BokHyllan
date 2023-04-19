from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Book
from . import db
import os

# variable för blueprint, detta lotta oss organiserat appen/programmet
views = Blueprint('views', __name__)

# route for homepage
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    books = Book.query.all()
    return render_template("home.html", user=current_user, books=books)


# detta är för att "edit profile" den är inte klart än.
@views.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def editprofile():
    return render_template('edit_profile.html', user=current_user)

# detta är så man lägger till en bok i databasen som sedan visas på home.html templaten.
@views.route('/add-book', methods=['GET', 'POST'])
@login_required
def addBook():
    if request.method == 'POST':
        title = request.form.get('title')
        review = request.form.get('review')
        new_book = Book(title=title, review=review, user_id=current_user.id)
        db.session.add(new_book)
        db.session.commit()
        flash('Boken har laddats upp!', category='success')
        return redirect(url_for('views.home'))
    return render_template('add_book.html', user=current_user)

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
    return redirect(url_for('views.home'))



# detta är för att ladda upp bilden. det är inte klart en det saknas förstarka "security" vi komma att göra det med werkzeug
@views.route('/add-pic', methods=['GET', 'POST'])
@login_required
def addpic():
    if request.method == "POST":
        if request.files:
            image = request.files['image']
            image.save(os.path.join("website\static\images", image.filename))
    return render_template('add_pic.html', user=current_user)


# detta är för att ladd upp biografi, detta är klart
@views.route('/add-bio', methods=['GET', 'POST'])
@login_required
def add_bio():
    if request.method == 'POST':
        new_bio = request.form.get('bio')
        bio_user = User.query.filter_by(id=current_user.id).first()
        bio_user.bio = new_bio
        db.session.commit()
        flash('Biografi har skopat!', category='success')
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