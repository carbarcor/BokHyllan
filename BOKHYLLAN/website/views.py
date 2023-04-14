from flask import Blueprint, render_template, request, flash,redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import User
from . import db
import json
import os

views = Blueprint('views', __name__)



@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    return render_template("home.html", user=current_user)


@views.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def editprofile():
     
     return render_template('edit_profile.html', user=current_user)


@views.route('/add-book', methods=['GET', 'POST'])
@login_required
def addBook():
     
     return render_template('add_book.html', user=current_user)

 


@views.route('/add-pic', methods=['GET', 'POST'])
@login_required
def addpic():
     
     if request.method == "POST":
          if request.files:
               image = request.files['image']
               image.save(os.path.join("website\static\images", image.filename))
     return render_template('add_pic.html', user=current_user)
        

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