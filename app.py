"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template, flash
# from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, User, db, Post, Tag

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
def show_homepage():
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
def handle_add_user():
    """Insert new user into db and redirects to users page."""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url'] or None

    user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(user)
    db.session.commit()

    flash('User added!')

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
def handle_edit_form(user_id):
    """Updates user information, commits to db and redirects to users."""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.img_url = img_url
    db.session.commit()

    flash('User updated!')

    return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def handle_delete_user(user_id):
    """Deletes user from db and redirects to users."""
    user = User.query.get_or_404(user_id)

    posts = Post.query.filter(Post.user_id == user_id).all()
    for post in posts:
        db.session.delete(post)

    db.session.delete(user)
    db.session.commit()

    flash('User deleted!')

    return redirect('/users')


@app.get('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Displays new post form."""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('new_post_form.html', user=user, tags=tags)


@app.post('/users/<int:user_id>/posts/new')
def handle_add_post(user_id):
    """Inserts new post into db and redirect to user detail page."""
    title = request.form['title']
    content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist('tag')]

    post = Post(title=title, content=content, user_id=user_id)

    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    flash('Post added!')

    return redirect(f'/users/{user_id}')


@app.get('/posts/<int:post_id>')
def show_post_detail(post_id):
    """Displays post detail"""
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.get('/posts/<int:post_id>/edit')
def show_post_edit_form(post_id):
    """Shows form to edit a post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)


@app.post('/posts/<int:post_id>/edit')
def handle_edit_post(post_id):
    """Handles post edit form submission and updates database accordingly"""
    title = request.form['title']
    content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist('tag')]

    post = Post.query.get_or_404(post_id)
    post.title = title
    post.content = content

    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.commit()

    flash('Post updated!')

    return redirect(f'/posts/{post_id}')


@app.post('/posts/<int:post_id>/delete')
def handle_delete_post(post_id):
    """Deletes a post"""
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    flash('Post deleted!')

    return redirect(f'/users/{post.user_id}')

@app.get('/tags')
def show_tag_list():
    """Displays list of all tags."""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.get('/tags/<int:tag_id>')
def show_tag_detail(tag_id):
    """Displays detail of tag."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag.html', tag=tag)

@app.get('/tags/new')
def show_new_tag_form():
    """Displays new tag form."""
    return render_template('new_tag_form.html')

@app.post('/tags/new')
def handle_add_tag():
    """Adds new tag to database."""
    name = request.form['tag_name']

    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()

    flash('Tag added!')

    return redirect('/tags')

@app.get('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """Shows form to edit a tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag_form.html', tag=tag)

@app.post('/tags/<int:tag_id>/edit')
def handle_edit_tag(tag_id):
    """Handles tag edit form submission and updates database accordingly"""
    name = request.form['tag_name']

    tag = Tag.query.get_or_404(tag_id)
    tag.name = name
    db.session.commit()

    flash('Tag updated!')

    return redirect('/tags')

@app.post('/tags/<int:tag_id>/delete')
def handle_delete_tag(tag_id):
    """Deletes a tag"""
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    flash('Tag deleted!')

    return redirect('/tags')