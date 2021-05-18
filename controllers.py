"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash, Field
from py4web.utils.url_signer import URLSigner
from .models import get_user_email
from py4web.utils.form import Form, FormStyleBulma
from pydal.validators import *

url_signer = URLSigner(session)

# SRC : https://bitbucket.org/luca_de_alfaro/class_registration/src/master/

# #######################################################
# Index
# #######################################################
@action('index')
@action.uses(db, auth.user, 'index.html')
def index():
    movie_rows = db((db.watch_list.watch_list_user_email == get_user_email())).select()
    return dict(rows=movie_rows, url_signer=url_signer)


# add_movie: to add a new entry. 
@action('add_movie', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'add_movie.html')
def add():
    form = Form(db.watch_list, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)

# edit_movie
@action('edit_movie/<watch_list_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, url_signer.verify(), 'edit_movie.html')
def edit(watch_list_id=None):
    assert watch_list_id is not None
    p = db.watch_list[watch_list_id]
    if p is None :
        # Nothing found to be edited
        redirect(URL('index'))

    form = Form(db.watch_list, record=p, deletable=False, csrf_session=session, formstyle=FormStyleBulma)

    if form.accepted:
        # The update already happened
        redirect(URL('index'))

    owner_info = db(db.watch_list.id == watch_list_id).select().first()
    if owner_info['watch_list_user_email'] == get_user_email():
        return dict(form=form)
    else:
        redirect(URL('index'))

@action('get_rating')
@action.uses(url_signer.verify(), db, auth.user)
def get_rating():
    """Returns the rating for a user and an image."""
    id = request.params.get('review_id')
    row = db((db.reviews.id == id) &
             (db.reviews.reviews_user_email == get_user_email())).select().first()
    rating = row.reviews_rating if row is not None else 0
    return dict(rating=rating)

@action('set_rating', method='POST')
@action.uses(url_signer.verify(), db, auth.user)
def set_rating():
    """Sets the rating for movie."""
    id = request.json.get('review_id')
    rating = request.json.get('rating')
    assert id is not None and rating is not None
    db.reviews.update_or_insert(
        ((db.reviews.id == id) & (db.reviews.reviews_user_email == get_user_email())),
        image=image_id,
        rater=get_user(),
        rating=rating
    )
    return "ok" # Just to have some confirmation in the Network tab.


# delete_movie
@action('delete_movie/<watch_list_id:int>')
@action.uses(db, session, auth.user, url_signer.verify())
def delete(watch_list_id=None):
    assert watch_list_id is not None
    owner_info = db(db.watch_list.id == watch_list_id).select().first()
    if owner_info['watch_list_user_email'] == get_user_email():
        db(db.watch_list.id == watch_list_id).delete()
    redirect(URL('index'))


# #######################################################
# Movie Reccomendations
# #######################################################
@action('movie_reccomendations')
@action.uses(db, auth.user, 'movie_reccomendations.html')
def movie_reccomendations():
    movie_rows = db((db.watch_list.watch_list_user_email == get_user_email())).select()
    return dict(rows=movie_rows, url_signer=url_signer)

# #######################################################
# Feed
# #######################################################
# TODO
# 1. Find a way to show only friends list's added movies with a timestamp similar to Twitter
@action('feed')
@action.uses(db, auth.user, 'feed.html')
def feed():
    movie_rows = db(db.watch_list).select()
    return dict(rows=movie_rows, url_signer=url_signer)

# #######################################################
# Notifications
# #######################################################
# TODO
# 1. Friend added/removed notification
# 2. Settings to show or not show friends added movies
@action('notifications')
@action.uses(db, auth.user, 'notifications.html')
def notifications():
    movie_rows = db((db.watch_list.watch_list_user_email == get_user_email())).select()
    return dict(rows=movie_rows, url_signer=url_signer)