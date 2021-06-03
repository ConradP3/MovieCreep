"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth, T
from pydal.validators import *

def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_user_name():
    first_name = auth.current_user.get('first_name') if auth.current_user else None
    last_name = auth.current_user.get('last_name') if auth.current_user else None
    return first_name + " " + last_name

def get_time():
    return datetime.datetime.utcnow()

def get_user():
    return auth.current_user.get('id') if auth.current_user else None
### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

# Planned/already Watched
    # Movie ID
    # User ID
    # Watched (Boolean)
# user_name = str(auth.current_user.get('first_name') )+ str(auth.current_user.get('last_name'))
r = db(db.auth_user.email == get_user_email).select().first()
name = r.first_name + " " + r.last_name if r is not None else "Unknown"
db.define_table(
    'watch_list',
    Field('movie_title', requires=IS_LENGTH(minsize=1)),
    Field('watch_list_watched'),
    Field('watch_list_date', 'date'),
    Field('watch_list_user_email', default=get_user_email),
    Field('watch_list_user_name', default=get_user_name),
    Field('watch_list_rating', 'integer', default=0),
    Field('watch_list_time_stamp', 'datetime', default=get_time),
    Field('watch_list_review')
)

# Reviews Table
    # Movie ID
    # User ID
    # Review
    # Rating
db.define_table(
    'review_comment',
    Field('watch_list_id', 'reference watch_list'),
    Field('user_email', default=get_user_email),
    Field('user_name', default=get_user_name),
    Field('comment', requires=IS_LENGTH(minsize=1))
)

# User Table
    # User ID
    # Movies/shows watched
    # Rating
    # Name/Email etc.
    # Friends list
    # When joined

db.define_table(
    'user',
    Field('user_name', default=get_user),
    Field('user_email', default=get_user_email),
    Field('user_id', default = get_user),
    Field('user_thumbnail')
)


db.define_table(
    'following',
    Field('following_user_name'),
    Field('following_user_email'),
    Field('following_thumbnail'),
    Field('following_id'),
    Field('reference')
)

db.define_table(
    'follower',
    Field('follower_user_name'),
    Field('follower_user_email'),
    Field('follower_thumbnail'),
    Field('follower_id'),
    Field('user_id')
)


db.watch_list.watch_list_time_stamp.readable = db.watch_list.watch_list_time_stamp.writable = False
db.watch_list.watch_list_user_name.readable = db.watch_list.watch_list_user_name.writable = False
db.watch_list.id.readable = db.watch_list.id.writable = False
db.watch_list.watch_list_user_email.readable = db.watch_list.watch_list_user_email.writable = False

db.review_comment.watch_list_id.readable = db.review_comment.watch_list_id.writable = False
db.review_comment.user_email.readable = db.review_comment.user_email.writable = False
db.review_comment.user_name.readable = db.review_comment.user_name.writable = False

db.watch_list.watch_list_watched.label = T('Seen')
db.watch_list.watch_list_rating.label = T('Your Movie Rating')
db.watch_list.watch_list_review.label = T('Your Movie Review')

db.commit()
