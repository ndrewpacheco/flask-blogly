"""Blogly application."""
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, render_template,  redirect, flash, session


app = Flask(__name__)
connect_db(app)
db.create_all()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "####"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def index():
    """index page redirects to users"""
    return redirect('/users')


@app.route('/users')
def show_listings():
    """displays all users"""
    title = "Users"
    users = User.query.all()
    return render_template('listings.html', title=title, users=users)


@app.route('/users/new')
def create_user():
    """Form for creating a user"""
    title = "Create A User"

    return render_template('create-user.html', title=title)


@app.route('/users/new', methods=["POST"])
def add_user_to_db():
    "adds user to db"
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    "Shows specific user by ID"
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Edit contents of user"""
    user = User.query.get_or_404(user_id)
    title = "Edit user"
    return render_template('edit-user.html', user=user, title=title)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def post_edit_user(user_id):
    """Saves edits of user"""
    user = User.query.get(user_id)

    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()
    return redirect('/')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """deletes user content"""
    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    return redirect('/')


# Posts routes

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    """show form to make new post"""
    user = User.query.get(user_id)
    return render_template('posts/create-post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def save_new_post(user_id):
    "save new post"
    title = request.form["post-title"]
    content = request.form["post-content"]

    new_post = Post(title=title,
                    content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """show post specified by post id"""
    post = Post.query.get(post_id)
    user = User.query.get(post.user_id)
    return render_template('posts/post.html', post=post, user=user)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """edit post"""
    post = Post.query.get(post_id)
    return render_template('posts/edit-post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def save_edit_post(post_id):
    """save edited post"""

    post = Post.query.get(post_id)
    post.title = request.form["post-title"]
    post.content = request.form["post-content"]

    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """deletes user content"""
    user_id = Post.query.get(post_id).user_id

    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()

    return redirect(f'/users/{user_id}')
