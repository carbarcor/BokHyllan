#denna handlar om användarautentisering.

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   
from flask_login import login_user, login_required, logout_user, current_user, login_manager
from sqlalchemy import update


'''Variabel för blueprint. Detta organiserar appen/programmet'''
auth = Blueprint('auth', __name__)

'''Funktion för radering av användarprofil'''
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


'''Funktion för redigering av användarprofil'''
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
            flash('Lösenordet är för kort, använd minst 8 tecken', category='error')
        elif len(new_name) < 1:
            flash('Du måste ange ett användarnamn', category='error')
        elif check_pw == False:
            flash('Det gamla lösenordet är inte korrekt, försök igen', category='error')
        else:
            db.session.commit()
            login_user(user, remember=True)
            flash('Profilen har uppdaterats!', category='success')
            return redirect(url_for('views.home'))
    
    return render_template("edit_profile.html", user=current_user)
    

'''Funktion för inloggning'''
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
                flash('Du är inloggad!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Felaktigt lösenord, försök igen', category='error')
        else:
            flash('Mejladressen finns inte, registrera dig för att kunna logga in', category='error')

    return render_template("login.html", user=current_user)


'''Funktion för utloggning, detta kommer fråm flask/loggin paket'''
@auth.route('/logout')
@login_required
#detta begränsa acces till user som har varit autetificierat
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


'''Funktion för registrering av användare'''
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Det finns redan en användare registrerad på mejladressen', category='error')
        elif len(email) < 5:
            flash('Mejladressen måste innehålla mer än 4 tecken', category='error')
        elif len(first_name) < 3:
            flash('Namnet måste innehålla minst 3 tecken', category='error')
        elif password1 != password2:
            flash('Lösenorden matchar inte, försök igen', category='error')
        elif len(password1) < 7:
            flash('Lösenordet är för kort, använd minst 8 tecken', category='error')
        else:
            new_user = User(email=email,
            first_name=first_name, 
            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Ditt konto har skapats!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)