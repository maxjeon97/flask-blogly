"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg"


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Users. A site has many users"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    img_url = db.Column(
        db.Text,
        nullable=False,  # could add a default image URL
        default=DEFAULT_IMAGE_URL
    )

    posts = db.relationship('Post', backref='user')

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class Post(db.Model):
    """Post. A user can have many posts."""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    def generate_readable_time(self):
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p %Z")

    tags = db.relationship('Tag', secondary='post_tags', backref='posts')


class Tag(db.Model):
    """A tag. A post can have many tags."""

    __tablename__ = "tags"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = db.Column(
        db.String(30),
        nullable=False,
        unique=True
    )


class PostTag(db.Model):
    """Through table for posts and tags."""

    __tablename__ = "post_tags"

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        primary_key=True
    )

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey('tags.id'),
        primary_key=True
    )
