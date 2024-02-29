"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
# from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, User, db, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# debug = DebugToolbarExtension(app)

connect_db(app)

@app.get('/')
def display_home_page():
    """Redirects to users page."""
    return redirect('/users')


@app.get('/users')
def show_users():
    """Displays users list."""
    users = User.query.all()
    return render_template('users.html', users=users)


@app.get('/users/new')
def show_new_user_form():
    """Displays new user form."""
    return render_template('new_user_form.html')


@app.post('/users/new')
def handle_submit():
    """Insert new user into db and redirects to users page."""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url'] or None

    user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.get('/users/<int:user_id>')
def show_user_info(user_id):
    """Displays user information."""
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user, posts=user.posts)

@app.get('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    """Displays edit user form."""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user_form.html', user=user)


@app.post('/users/<int:user_id>/edit')
def process_edit_form(user_id):
    """Updates user information, commits to db and redirects to users."""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.img_url = img_url
    db.session.commit()

    return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Deletes user from db and redirects to users."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
@app.get('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Displays new post form."""
    user = User.query.get_or_404(user_id)
    return render_template('new_post_form', user=user)

@app.post('/users/<int:user_id>/posts/new')
def add_new_post(user_id):
    """Insert new post into db and redirect to post page."""
    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user_id = user_id)
    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')
