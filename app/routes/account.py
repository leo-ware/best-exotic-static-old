
from app import app
from app.models import User

from flask import render_template, request, redirect, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.exceptions import BadRequest


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('account/dashboard.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            flash("You are already logged in.")
            return redirect('/')
        return render_template('account/login.html')
    elif request.method == 'POST':
        print(request.form)
        password = request.form['password']
        print(password)
        email = request.form['email']
        print(email)

        try:
            remember_me = bool(request.args['remember_me'])
        except KeyError:
            remember_me = False

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember_me)
            flash("Login successful")
        elif not user:
            flash("Login Error", "No user was found with that email.")
            redirect('/login')
        else:
            flash("Login Error", "The password you entered is incorrect.")
            redirect('/login')

        return redirect('/')


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("You are logged out.")
    else:
        flash("You are not logged in.")
    return redirect('/')
