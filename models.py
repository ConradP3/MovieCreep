"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth, T
from pydal.validators import *

import os

MOVIE_DB_PATH = os.path.dirname(os.path.abspath(__file__)) + '/mdb.csv'


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

# Movie Table
    # Movie ID
    # Title
    # Avg rating
    # Genre
    # Img
    # src watched at
    # release date
    # Country
    # Language
db.define_table(
    'movies',
    Field('title'),
    Field('rating'),
    Field('genres'),
    Field('img'),
    Field('releasedate'),
    Field('country'),
    Field('language')
)


# Planned/already Watched
    # Movie ID
    # User ID
    # Watched (Boolean)
db.define_table(
    'watch_list',
    Field('movie_id', 'reference movies'),
    Field('movie_title', requires=IS_LENGTH(minsize=1)),
    Field('watch_list_date', 'date'),
    Field('watch_list_user_email', default=get_user_email),
    Field('watch_list_watched', 'boolean'),
    Field('watch_list_rating', 'integer', default=0),
    Field('watch_list_time_stamp', 'datetime', default=get_time)
)


# Reviews Table
    # Movie ID
    # User ID
    # Review
    # Rating
db.define_table(
    'reviews',
    Field('movie_id', 'reference movies'),
    Field('watch_listid', 'reference watch_list'),
    Field('reviews_user_email', default=get_user_email),
    Field('reviews_review'),
    Field('reviews_rating')
)

# User Table
    # User ID
    # Movies/shows watched
    # Rating
    # Name/Email etc.
    # Friends list
    # When joined



db.watch_list.watch_list_time_stamp.readable = db.watch_list.watch_list_time_stamp.writable = False
db.watch_list.id.readable = db.watch_list.id.writable = False
db.watch_list.movie_id.readable = db.watch_list.movie_id.writable = False
db.watch_list.watch_list_user_email.readable = db.watch_list.watch_list_user_email.writable = False

db.watch_list.watch_list_watched.label = T('Seen')


db.commit()

with open(MOVIE_DB_PATH, 'r', encoding='utf-8', newline='') as movies_csv:
    db.movies.import_from_csv_file(movies_csv)
