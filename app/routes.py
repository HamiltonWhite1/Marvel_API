from app import app, db
from flask import Flask, url_for, render_template, redirect, flash
from flask_login import current_user, login_user, logout_user
from app.models import Hero, User
from app.forms import LoginForm, RegistrationForm, CreateHeroForm
import json


@app.route('/')
def front_page():
    return render_template('front_page.html', title='Welcome')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('front_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('front_page'))
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('front_page'))

@app.route('/register', methods=['GET', 'POST']) #user registration now working, but I had to disable the class for the Hero table
def register():
    if current_user.is_authenticated:
        return redirect(url_for('front_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome to Build Your Own Avengers')
        return redirect('login')
    return render_template('register.html', title='Register', form=form)

@app.route('/create_heroes', methods=['GET', 'POST']) #logic of the following function "works" but is not committing changes to DataBase
def create_heroes():
    form = CreateHeroForm()
    if form.validate_on_submit():
        new_hero = Hero(name=form.name.data, description=form.description.data)
        db.session.add(new_hero)
        db.session.commit()
    return render_template('create_heroes.html', title='Create Heroes', form=form)

@app.route('/API')
def API():
    marvel_dict_dict = {
        'Heroes' : [
            {'Ant-Man': 'Turns into an ant. It kinda goes without saying.'},
            {'Spiderman': 'Shoots web out of his wrists'},
            {'Thor': 'Beautiful blond man. He has a hammer. And shoots lightning'},
            {'Iron Man': "Uber rich narcissist's heart gives out while in military captivity, so he rips his heart out or something crazy and puts a nuclear reactor into it. Now he's dead, I think?"},
            {'Captain Marvel': "Bruce Willis-type actress that random-internet-man says should 'learn to smile more often'. Can fly really awesome planes and punch the hell out of people. I think. She like turns into the sun or something and becomes an inter-galactic cosmic space-god."},
            {'Hawk Eye': "Self-indulgent backstreet boy takes 'cowboys and indians' from his childhood way too seriously, goes on to become the least interesting Avenger with the highest sense of self-worth. Makes his own social-media platform so that his fans can engage with him in real life."},
            {'Black Panther': "King wasn't rich and powerful enough, so his genius sister builds a suit for him to turn into a kitty-kat with. 10/10 cosplay hero"}

        ],
        'Marvel Film and TV IP': [
            {'i-Robot': 'Thor fights a weird lady with a black head-piece that makes her look like a deer. Pretty robotic character, not much charisma'},
            {'Good Will Hunting': 'Robot Downey JR is going through life, wondering why the world is looking down on him and his billions of dollars and his totally crazy mech suit that could frankly incinerate an entire nation-state. It is all the more awful for Robot JR because he keeps wondering why everyone calls him Will, and wonders why Robin Williams keeps telling him its not his fault. 6/10'},
            {"The Black Panther": "Villian goes on to make the most compelling moral argument in the entire film, as the trillion-dollar multi-national corp. that produces the movie kills him without a hint of irony and instantaneously washes itself of any class consciousness and moral righteousness. Money good. Poors bad."},
            {"Punisher": "Man scarred by police corruption goes on murderous rampage against organized crime bosses and police/military officers, as corrupt police/military officers in real life sew his patch into their shirts and murder ordinary people."}
        ]
    }
    return marvel_dict_dict