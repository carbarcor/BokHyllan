from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import update



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
    
# detta är för att "edit profile" den är klart att köra nu.
@auth.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        user = User.query.filter_by(id=current_user.id).first()
        new_name = request.form.get('new_name')
        new_password = request.form.get('new_password')
        old_password = request.form.get('old_password')    
        user.first_name = new_name
        hash_pw = generate_password_hash(new_password, method='sha256')
        check_pw = check_password_hash(user.password, old_password)
        user.password = hash_pw
        
        if len(new_password) < 7:
            flash('Lösenord är för kort, minst 8 tecken', category='error')
        elif len(new_name) < 1:
            flash('Namnet är för kort', category='error')
        elif check_pw == False:
            flash('Det gamla lösenordet är inte korrekt!', category='error')
        else:
            db.session.commit()
            login_user(user, remember=True)
            flash('Profilen har uppdaterats!', category='success')
            return redirect(url_for('views.home'))
    
    return render_template("edit_profile.html", user=current_user)
    
    



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
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



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


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

