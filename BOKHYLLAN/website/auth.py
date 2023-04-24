#denna handlar om användarautentisering.

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import update


#hjälpa att organiserat bätter väggarna "path"
auth = Blueprint('auth', __name__)


@auth.route('/delete_profile' , methods=['GET', 'POST'])
@login_required
def delete_profile():
    id = User.id
    if request.method == 'POST':
        user = User.query.filter_by(id=current_user.id).first()
        db.session.delete(user)
        db.session.commit()
        logout_user()
        return redirect(url_for('auth.login',user=current_user))
    

@auth.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        id = User.id
        user = User.query.filter_by(id=current_user.id).first()
        if user:
            old_password = request.form.get("old_password")
            new_name = request.form.get("new_name")
            new_password = request.form.get("new_password") 
            hash_new_password = generate_password_hash(new_password, method='sha256')
            user.first_name = new_name
            user.password = hash_new_password
            db.session.commit()
            flash('Kontouppgradering!', category='success')
            return redirect(url_for('auth.login'))
    



#detta köra logg in
@auth.route('/login', methods=['GET', 'POST'])
def login():
    """hämta data from html"""
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        """detta kontrolerra om det finns i databasen är det så kan du logga in (logga in funtionen finns redan i falsk)"""
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


#detta logga ut
@auth.route('/logout')
@login_required
#detta begränsa acces till user som har varit autetificierat
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#resgiterat user
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('account exist', category='error')
        elif len(email) < 5:
            flash('Mejladressen måste vara mer en 4 bokstovlar', category='error')
        elif len(first_name) < 3:
            flash('Namnet är för kort', category='error')
        elif password1 != password2:
            flash('Lösenord matchar inte', category='error')
        elif len(password1) < 3:
            flash('Lösenord måste ha mer en 2 tecken, försök igen!', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Skapa konto!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

