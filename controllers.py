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

import json
import requests
import uuid
import random
url_signer = URLSigner(session)
apikeys = ['8fb72c1a', '2710f070']

# SRC : https://bitbucket.org/luca_de_alfaro/class_registration/src/master/

# #######################################################
# Index
# #######################################################
@action('index')
@action.uses(db, auth.user, 'index.html')
def index():
    movie_rows = db((db.watch_list.watch_list_user_email == get_user_email())).select()
    # print(movie_rows)
    for m in movie_rows:
        link = ''
        plot = ''
        runtime = ''
        rating = ''
        releasedate = ''
        imdbrating = ''
        genre = ''

        url = 'http://www.omdbapi.com/?t=' + str(m['movie_title']) + '&apikey=' + apikeys[random.randint(0,len(apikeys)-1)]
        movie_data = requests.get(url).json()
        # r = requests.get(url)
        # Check for this or else user's account can get bricked
        if movie_data['Response'] != "False":
            link += str(movie_data['Poster'])
            plot += str(movie_data['Plot'])
            runtime += str(movie_data['Runtime'])
            rating += str(movie_data['Rated'])
            releasedate += str(movie_data['Released'])
            # imdbrating += str(movie_data['imdbRating'])
            genre += str(movie_data['Genre'])
        else:
            plot += "Movie not found when attempting to contact omdbapi"
        m['link'] = link
        m['genre'] = genre
        # m['imdbrating'] = imdbrating
        m['releasedate'] = releasedate
        m['rating'] = rating
        m['runtime'] = runtime
        m['plot'] = plot

            
        # https://api.themoviedb.org/3/movie/550?api_key=fa5fa1a7dd403108f2c44bf79fca3f2f

        # https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg
        # http://www.omdbapi.com/?t=interstellar&apikey=2710f070


    print(movie_rows)
    return dict(rows=movie_rows, url_signer=url_signer,
                add_movie_url = URL('add_movie', signer=url_signer),
                get_rating_url = URL('get_rating', signer=url_signer),
                set_rating_url = URL('set_rating', signer=url_signer),
                search_url = URL('search', signer=url_signer),
                user_email=get_user_email())


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

# @action('get_rating')
# @action.uses(url_signer.verify(), db, auth.user)
# def get_rating():
#     """Returns the rating for a user and an image."""
#     id = request.params.get('review_id')
#     row = db((db.reviews.id == id) &
#              (db.reviews.reviews_user_email == get_user_email())).select().first()
#     rating = row.reviews_rating if row is not None else 0
#     return dict(rating=rating)

# @action('set_rating', method='POST')
# @action.uses(url_signer.verify(), db, auth.user)
# def set_rating():
#     """Sets the rating for movie."""
#     id = request.json.get('review_id')
#     rating = request.json.get('rating')
#     assert id is not None and rating is not None
#     db.reviews.update_or_insert(
#         ((db.reviews.id == id) & (db.reviews.reviews_user_email == get_user_email())),
#         image=image_id,
#         rater=get_user(),
#         rating=rating
#     )
#     return "ok" # Just to have some confirmation in the Network tab.


# delete_movie
@action('delete_movie/<watch_list_id:int>')
@action.uses(db, session, auth.user, url_signer.verify())
def delete(watch_list_id=None):
    assert watch_list_id is not None
    owner_info = db(db.watch_list.id == watch_list_id).select().first()
    if owner_info['watch_list_user_email'] == get_user_email():
        db(db.watch_list.id == watch_list_id).delete()
    redirect(URL('index'))


@action('search')
@action.uses()
def search():
    q = request.params.get("q")
    results = [q + ":" + str(uuid.uuid1()) for _ in range(random.randint(2, 6))]
    #if (q in movierows)
    #add row to results
    #print results
    return dict(results = results)
#return movie rows that contain q

# #######################################################
# Movie Reccomendations
# #######################################################
@action('movie_reccomendations')
@action.uses(db, auth.user, 'movie_reccomendations.html')
def movie_reccomendations():
    movie_rows = db((db.watch_list.watch_list_user_email != get_user_email())).select()
    # print(movie_rows)
    for m in movie_rows:
        link = ''
        plot = ''
        runtime = ''
        rating = ''
        releasedate = ''
        imdbrating = ''
        genre = ''

        url = 'http://www.omdbapi.com/?t=' + str(m['movie_title']) + '&apikey=' + apikeys[random.randint(0,len(apikeys)-1)]
        movie_data = requests.get(url).json()
        # r = requests.get(url)
        link += str(movie_data['Poster'])
        plot += str(movie_data['Plot'])
        runtime += str(movie_data['Runtime'])
        rating += str(movie_data['Rated'])
        releasedate += str(movie_data['Released'])
        # imdbrating += str(movie_data['imdbRating'])
        genre += str(movie_data['Genre'])
        m['link'] = link
        m['genre'] = genre
        # m['imdbrating'] = imdbrating
        m['releasedate'] = releasedate
        m['rating'] = rating
        m['runtime'] = runtime
        m['plot'] = plot



    print(movie_rows)
    return dict(rows=movie_rows, url_signer=url_signer,
                add_movie_url = URL('add_movie', signer=url_signer),
                get_rating_url = URL('get_rating', signer=url_signer),
                set_rating_url = URL('set_rating', signer=url_signer),
                user_email=get_user_email())

# #######################################################
# Feed
# #######################################################
# TODO
# 1. Find a way to show only friends list's added movies with a timestamp similar to Twitter
@action('feed')
@action.uses(db, auth.user, 'feed.html')
def feed():
    movie_rows = db(db.watch_list).select()
    # print(movie_rows)
    for m in movie_rows:
        link = ''
        plot = ''
        runtime = ''
        rating = ''
        releasedate = ''
        imdbrating = ''
        genre = ''

        url = 'http://www.omdbapi.com/?t=' + str(m['movie_title']) + '&apikey=' + apikeys[random.randint(0,len(apikeys)-1)]
        movie_data = requests.get(url).json()
        # r = requests.get(url)
        if movie_data['Response'] != 'False':
            link += str(movie_data['Poster'])
            plot += str(movie_data['Plot'])
            runtime += str(movie_data['Runtime'])
            rating += str(movie_data['Rated'])
            releasedate += str(movie_data['Released'])
            # imdbrating += str(movie_data['imdbRating'])
            genre += str(movie_data['Genre'])
        else:
            # See index controller comments
            plot = 'Movie was not found when trying to contact omdbapi.'
        m['link'] = link
        m['genre'] = genre
        # m['imdbrating'] = imdbrating
        m['releasedate'] = releasedate
        m['rating'] = rating
        m['runtime'] = runtime
        m['plot'] = plot

    

    print(movie_rows)
    return dict(rows=movie_rows, url_signer=url_signer,
                add_movie_url = URL('add_movie', signer=url_signer),
                get_rating_url = URL('get_rating', signer=url_signer),
                set_rating_url = URL('set_rating', signer=url_signer),
                user_email=get_user_email(),
                 )

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

# #######################################################
# Profile
# #######################################################
# TODO
# 1. Find a way to display list of all friends
@action('profile')
@action.uses(db, auth.user, 'profile.html')
def profile():
    rows = db(db.user.user_email == get_user_email()).select()
    first_name = auth.current_user.get('first_name')
    last_name = auth.current_user.get('last_name')
    name = first_name + " " + last_name
    email = get_user_email()
    return dict(rows=rows, name=name, email=email, 
                file_upload_url = URL('file_upload', signer=url_signer),
                search_url=URL('search_friends', signer=url_signer))

@action('file_upload', method="PUT")
@action.uses(db) # Add here things you might want to use.
def file_upload():
    file_name = request.params.get("file_name")
    file_type = request.params.get("file_type")
    uploaded_file = request.body # This is a file, you can read it.
    # Diagnostics
    print("Uploaded", file_name, "of type", file_type)
    print("Content:", uploaded_file.read())
    return "ok"

@action('search_friends')
@action.uses(db, auth)
def search_friends():
    #q = request.params.get("q")
    #rows = db(db.auth_user.email == q).select()

    #for row in rows:
    #    results = row['first_name'] + " " + row['last_name'] + " " + row['email']
    #print(results)

    q = request.params.get("q")
    resultsrows = db(db.auth_user.email == q).select()
    for r in resultsrows:
        output = r['first_name'] + " " + r['last_name'] + " " + r['email']
        friend_id = r['id']

    results = [output]
    print(friend_id)

    return dict(results = results, friend_id=friend_id)

@action('add_following')
@action.uses(db, session, auth.user)
def add():
    rows = db(db.user.user_email == get_user_email()).select()

    return dict(rows)
