"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


# MODELS
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50),
                           nullable=False,
                           unique=False)

    last_name = db.Column(db.String(50),
                          nullable=False,
                          unique=False)

    image_url = db.Column(db.String(), nullable=True)

    def __repr__(self):
        p = self
        return f"<User id={p.id} first_name={p.first_name} last_name={p.last_name}>"


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(),
                      nullable=False,
                      unique=False)

    content = db.Column(db.String(),
                        nullable=False,
                        unique=False)

    created_at = db.Column(db.DateTime(), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='posts')

    tags = db.relationship('Tag',
                           secondary='posts_tags',
                           backref='posts')

    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} content={p.content}>"


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.String(),
                     nullable=False,
                     unique=True)


class PostTag(db.Model):

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id"),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey("tags.id"),
                       primary_key=True)
