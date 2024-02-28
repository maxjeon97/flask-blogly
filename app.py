"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, User, db

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.get('/')
def display_list_of_users():
    return redirect('/users')

@app.get('/users')
def show_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.get('/users/new')
def show_new_user_form():
    return render_template('new_user_form.html')

@app.post('/users/new')
def handle_submit():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    user = User(first_name = first_name, last_name = last_name, img_url = img_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get(user_id)
    return render_template('user.html', user=user)

@app.get('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    user = User.query.get(user_id)
    return render_template('edit_user_form.html', user=user)

@app.post('/users/<int:user_id>/edit')
def process_edit_form(user_id):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.img_url = img_url
    db.session.commit()

    return redirect('/users')

@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):

