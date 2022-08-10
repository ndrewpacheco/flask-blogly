"""Seed file to make sample data for pets db."""

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
whiskey = User(first_name='Whiskey', last_name='W',
               image_url="https://uploads.concordia.net/2017/08/30180948/headshot-placeholder.jpg")
bowser = User(first_name='Bowser', last_name='Bow',
              image_url="https://uploads.concordia.net/2017/08/30180948/headshot-placeholder.jpg")
spike = User(first_name='Spike', last_name='S',
             image_url="https://uploads.concordia.net/2017/08/30180948/headshot-placeholder.jpg")


# Add new objects to session, so they'll persist
db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)

# Commit--otherwise, this never gets saved!
db.session.commit()


# Add posts
new_post1 = Post(title='New post 1', content='1 some post content', user_id=1)
new_post2 = Post(title='New post 2', content='2 some post content', user_id=2)

# Add new objects to session, so they'll persist
db.session.add(new_post1)
db.session.add(new_post2)


# Commit--otherwise, this never gets saved!
db.session.commit()
