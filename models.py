"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *

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
# Reviews Table
    # Movie ID
    # User ID
    # Review
    # Rating
db.define_table(
    'reviews',
    Field('movie_id', 'reference movies'),
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


# Planned/already Watched
    # Movie ID
    # User ID
    # Watched (Boolean)
db.define_table(
    'watch_list',
    Field('movie_id', 'reference movies'),
    Field('movie_title'),
    Field('watch_list_user_email', default=get_user_email),
    Field('watch_list_watched', 'boolean')
)


db.commit()

with open('apps/MovieCreep/mdb.csv', 'r', encoding='utf-8', newline='') as movies_csv:
    db.movies.import_from_csv_file(movies_csv)
