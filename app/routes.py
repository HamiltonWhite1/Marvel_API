from app import app
from flask import Flask, url_for, render_template, redirect, flash
from flask_login import current_user, login_user, logout_user
from app.models import User
from app.forms import LoginForm


@app.route('/')
def front_page():
    return render_template('front_page.html', title='Welcome')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html', title='Login')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))