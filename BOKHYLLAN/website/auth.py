#denna handlar om användarautentisering.

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   
from flask_login import login_user, login_required, logout_user, current_user


#hjälpa att organiserat bätter väggarna "path"
auth = Blueprint('auth', __name__)

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
                flash('Användare inloggad.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Felaktigt lösenord, försök igen.', category='error')
        else:
            flash('E-post saknas.', category='error')

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
            flash('Användarkontot finns redan.', category='error')
        elif len(email) < 5:
            flash('Mejladressen måste vara längre än 4 bokstäver.', category='error')
        elif len(first_name) < 3:
            flash('Namnet är för kort.', category='error')
        elif password1 != password2:
            flash('Lösenorden matchar inte.', category='error')
        elif len(password1) < 3:
            flash('Lösenordet måste ha fler än 2 tecken, försök igen!', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Användarkonto skapat.', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

