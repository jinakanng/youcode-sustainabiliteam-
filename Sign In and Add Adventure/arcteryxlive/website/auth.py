from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.models import User
from flask_login import login_user, login_required, logout_user, current_user

# to ensure password is never stored as plain text: can't get back to password from hash (hash is smt that doesn't have an inverse)
from werkzeug.security import generate_password_hash, check_password_hash
from . import db # imports database from __init__.py


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!', category='success')
                login_user(user, remember=True)
                # redirects to home page
                return redirect(url_for('views.home'))
            else: 
                flash('Incorrect password, try again.', category='error')
                

    return render_template("login.html", user=current_user)

@auth.route('/logout')
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
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be atleast 1 character.', category= 'error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category= 'error')
        elif len(password1) < 7:
            flash('Password must be atleast 7 characters.', category= 'error')
        else:
            # creates new user
            new_user = User(email=email, first_name=first_name,password=generate_password_hash(password1, method = 'pbkdf2:sha256'))
            # successfully add user to database
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created. May the adventures begin.', category= 'success')
            # redirects to home page
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
