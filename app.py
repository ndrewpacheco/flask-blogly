"""Blogly application."""
from models import db, connect_db, User
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
    return redirect('/users')


@app.route('/users')
def show_listings():
    title = "Users"
    users = User.query.all()
    return render_template('listings.html', title=title, users=users)


@app.route('/users/new')
def create_user():
    title = "Create A User"

    return render_template('create-user.html', title=title)


@app.route('/users/new', methods=["POST"])
def add_user_to_db():
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
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    title = "Edit user"
    return render_template('edit-user.html', user=user, title=title)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def post_edit_user(user_id):
    user = User.query.get(user_id)

    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()
    return redirect('/')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    return redirect('/')
