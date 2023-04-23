#Views, skapar vägarna för att navigiera runt på webbplatsen.
#olika paketer som vi behöver ladda ner så programmet kan köra.
from flask import Blueprint, render_template, request, flash,redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import User
from . import db
import json
import os

#variable för blueprint, detta lotta oss organiserat appen/programmet
views = Blueprint('views', __name__)


#Route för sidan home.html
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

     return render_template("home.html", user=current_user)


#detta är för att "edit profile" den är inte klart än.
@views.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def editprofile():
     
     return render_template('edit_profile.html', user=current_user)


#detta är för att ladda upp en bok, detta är inte klart än.
@views.route('/add-book', methods=['GET', 'POST'])
@login_required
def addBook():
     
     return render_template('add_book.html', user=current_user)

 

"""detta är för att ladda upp bilden. det är inte klart en det saknas förstarka "security" vi komma att göra det med werkzeug"""
@views.route('/add-pic', methods=['GET', 'POST'])
@login_required
def addpic():
     
     if request.method == "POST":
          if request.files:
               image = request.files['image']
               image.save(os.path.join("website\static\images", image.filename))
     return render_template('add_pic.html', user=current_user)
        
"""detta är för att ladd upp biografi, detta är klart"""
@views.route('/add-bio', methods=['GET', 'POST'])
@login_required
def addBio():
        if request.method == 'POST':
            new_bio = request.form.get('bio')
            bio_user = User.query.filter_by(id=current_user.id).first()
            bio_user.bio = new_bio
            db.session.commit()
            flash('Biografi har skopat!', category='success')
            return redirect(url_for('views.home'))
        
        return render_template("add_bio.html", user=current_user)

"""detta är för att radera bio, den är inte implementera än för att vet inte om det behövs
@views.route('/delete-bio', methods=['POST'])
def delete_bio():
    bio = json.loads(request.data)
    bioId = bio['bioId']
    bio = Bio.query.get(bioId)
    if bio:
        if bio.user_id == current_user.id:
            db.session.delete(bio)
            db.session.commit()
            return jsonify({})"""