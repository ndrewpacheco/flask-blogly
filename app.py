"""Blogly application."""

from models import db, connect_db, User, Post, Tag
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, render_template, redirect


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


@app.route('/users', methods=["POST"])
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
    title = f"{user.first_name} {user.last_name}"
    return render_template('user.html', user=user, title=title)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Edit contents of user"""

    user = User.query.get_or_404(user_id)
    title = "Edit user"
    return render_template('edit-user.html', user=user, title=title)


@app.route('/users/<int:user_id>', methods=['POST'])
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
    tags = Tag.query.all()
    return render_template('posts/create-post.html', tags=tags, user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def save_new_post(user_id):
    "save new post"
    title = request.form["post-title"]
    content = request.form["post-content"]
    tags = request.form.getlist('post-tags')

    new_post = Post(title=title,
                    content=content, user_id=user_id)

    for tag in tags:
        new_tag = Tag.query.filter(Tag.name == tag).first()
        if new_tag is None:
            new_tag = Tag(name=tag)
        new_post.tags.append(new_tag)

    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """show post specified by post id"""
    post = Post.query.get(post_id)
    user = User.query.get(post.user_id)
    tags = post.tags
    return render_template('posts/post.html', tags=tags, post=post, user=user)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """edit post"""
    post = Post.query.get(post_id)
    tags = Tag.query.all()

    return render_template('posts/edit-post.html', tags=tags, post=post)


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


# Tags routes
@app.route('/tags')
def show_tags():
    """Lists all tags, with links to the tag detail page."""

    title = 'Tags'
    tags = Tag.query.all()
    return render_template('tags/tags.html', tags=tags, title=title)


@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Show detail about a tag. Show links to edit form and to delete."""

    tag = Tag.query.get(tag_id)
    title = tag.name
    posts = tag.posts
    return render_template('tags/tag.html', posts=posts, tag=tag, title=title)


@app.route('/tags/new')
def create_tag():
    """Shows a form to add a new tag."""

    title = 'Create a tag'
    return render_template('tags/create-tag.html', title=title)


@app.route('/tags/new', methods=['POST'])
def post_tag():
    """creates new tag."""

    name = request.form["name"]

    new_tag = Tag(name=name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Shows a form to add a new tag."""

    title = 'Edit a tag'
    tag = Tag.query.get(tag_id)
    return render_template('tags/edit-tag.html', title=title, tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def post_edited_Tag(tag_id):

    tag = Tag.query.get(tag_id)
    tag.name = request.form["name"]
    db.session.add(tag)
    db.session.commit()

    return redirect(f'/tags/{tag_id}')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """deletes tag"""

    Tag.query.filter(Tag.id == tag_id).delete()
    db.session.commit()

    return redirect(f'/tags')
