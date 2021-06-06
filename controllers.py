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
from .models import get_user_email, get_time, get_user_name, get_user
from py4web.utils.form import Form, FormStyleBulma
from pydal.validators import *


import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import os

import json
import requests
import uuid
import random
url_signer = URLSigner(session)
apikeys = ['8fb72c1a', '2710f070']

CSV_PATH = os.path.dirname(os.path.abspath(__file__)) + '/movies.csv'


# SRC : https://bitbucket.org/luca_de_alfaro/class_registration/src/master/

# #######################################################
# Index
# #######################################################
@action('index')
@action.uses(db, auth.user, 'index.html')
def index():
    movie_rows = db((db.watch_list.watch_list_user_email == get_user_email())).select()
    user_rows = db(db.user.user_email).select() # All users
    likes_rows = db(db.likes.likes_user_email).select() # All likes
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

        # Get the review comments for the movie
        comment_rows = db(db.review_comment.watch_list_id == m['id']).select()
        # Also get the profile pictures
        for comment in comment_rows:
            user_row = db(db.user.user_email == comment['user_email']).select().first()
            thumbnail_link = user_row['user_thumbnail']
            if thumbnail_link == None:
                thumbnail_link == "https://www.jing.fm/clipimg/detail/195-1952632_account-customer-login-man-user-icon-login-icon.png"
            comment['thumbnail'] = thumbnail_link
        m['comments'] = comment_rows

        m['thumbnail'] = None
        m['rating'] = -1

        # https://api.themoviedb.org/3/movie/550?api_key=fa5fa1a7dd403108f2c44bf79fca3f2f

        # https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg
        # http://www.omdbapi.com/?t=interstellar&apikey=2710f070
        for user in user_rows:
            if user['user_email'] == m['watch_list_user_email']:
                m['thumbnail'] = user['user_thumbnail']

        for like in likes_rows:
            if like['likes_user_email'] == m['watch_list_user_email'] and like['likes_movie'] == m['id']:
                m['rating'] = like['rating']



    print(movie_rows)
    return dict(rows=movie_rows, url_signer=url_signer,
                add_movie_url = URL('add_movie', signer=url_signer),
                get_rating_url = URL('get_rating', signer=url_signer),
                set_rating_url = URL('set_rating', signer=url_signer),
                search_url = URL('search', signer=url_signer),
                get_comments_url = URL('get_comments', signer=url_signer),
                user_email=get_user_email(),
                user_name=get_user_name())


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

@action('set_rating/<id:int>/<rating:int>',  method=["GET", "POST"])
@action.uses(url_signer.verify(), db, auth.user)
def set_rating(id, rating):
    """Sets the rating for movie."""
    assert id is not None and rating is not None
    db.likes.update_or_insert(
        likes_movie=id,
        rating=rating,
        likes_liker=get_user(),
        likes_name=get_user_name(),
        likes_user_email=get_user_email,
    )
    redirect(URL('index'))
                # Field('likes_movie', 'reference watch_list'), # Movie liked
                # Field('rating', 'integer', default=-1),
                # Field('likes_liker', 'reference auth_user'), # User doing the like.
                # Field('likes_name'),
                # Field('likes_user_email', default=get_user_email),

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
    results = db(db.watch_list.movie_title == q).select().as_list()

    return dict(results = results)
#return movie rows that contain q

# #######################################################
# Movie Reccomendations
# #######################################################
@action('movie_reccomendations')
@action.uses(db, auth.user, 'movie_reccomendations.html')
def movie_reccomendations():
    recommended_list = []

    movieData = pd.read_csv(CSV_PATH)
    movieData['description'] = movieData['overview'] + movieData['tagline']
    movieData['description'].fillna(value='', inplace=True)
    
    tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(movieData['description'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)              # Measure of similarity between two movies

    titles = movieData['title']
    indices = pd.Series(movieData.index, index=movieData['title'])

    # Get similar movies based on description of movie added to user profile
    def get_recommendations(title):
        similarities = sorted(list(enumerate(cosine_sim[indices[title]])), key=lambda x: x[1], reverse=True)[1:31]
        movie_indices = [i[0] for i in similarities]
        return titles.iloc[movie_indices]
  
    

    users_added_movies = db((db.watch_list.watch_list_user_email == get_user_email())).select()
    for movie in users_added_movies:
        try:
            recommended = get_recommendations(movie['movie_title']).sample()
            recommended_list = recommended.to_list()
            movie['recommended'] = recommended_list

            link = ''
            plot = ''
            runtime = ''
            rating = ''
            releasedate = ''
            imdbrating = ''
            genre = ''
            url = 'http://www.omdbapi.com/?t=' + str(movie['recommended']) + '&apikey=' + apikeys[random.randint(0,len(apikeys)-1)]
            movie_data = requests.get(url).json()
            if movie_data['Response'] != "False":
                link += str(movie_data['Poster'])
                plot += str(movie_data['Plot'])
                runtime += str(movie_data['Runtime'])
                rating += str(movie_data['Rated'])
                releasedate += str(movie_data['Released'])
                genre += str(movie_data['Genre'])
            else:
                plot = 'Movie was not found when trying to contact omdbapi.'
                movie['recommended'] = None
            movie['link'] = link
            movie['genre'] = genre
            movie['releasedate'] = releasedate
            movie['rating'] = rating
            movie['runtime'] = runtime
            movie['plot'] = plot


        except:
            print("Movie Recommendations: " + str(movie['movie_title']) + " Not Recognized")
            movie['recommended'] = None
            movie['link'] = None
            movie['genre'] = None
            movie['releasedate'] = None
            movie['rating'] = None
            movie['runtime'] = None
            movie['plot'] = None
            pass

     

    movie_rows = db((db.watch_list.watch_list_user_email != get_user_email())).select()
    print(movie_rows)
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
        if movie_data['Response'] != "False":
            link += str(movie_data['Poster'])
            plot += str(movie_data['Plot'])
            runtime += str(movie_data['Runtime'])
            rating += str(movie_data['Rated'])
            releasedate += str(movie_data['Released'])
            # imdbrating += str(movie_data['imdbRating'])
            genre += str(movie_data['Genre'])
        else:
            plot = 'Movie was not found when trying to contact omdbapi.'
        m['link'] = link
        m['genre'] = genre
        # m['imdbrating'] = imdbrating
        m['releasedate'] = releasedate
        m['rating'] = rating
        m['runtime'] = runtime
        m['plot'] = plot



    print(movie_rows)
    return dict(rows=movie_rows,
                content_based_recommendations=users_added_movies,
                url_signer=url_signer,
                quick_add_movie_url = URL('quick_add_movie', signer=url_signer),
                add_movie_url = URL('add_movie', signer=url_signer),
                get_rating_url = URL('get_rating', signer=url_signer),
                set_rating_url = URL('set_rating', signer=url_signer),
                user_email=get_user_email())

# quick_add_movie: to add a new entry in watch_list of the recommended movie
@action('quick_add_movie/<movie_title>', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'add_movie.html')
def quick_add(movie_title):
    db.watch_list.insert(movie_title=movie_title, 
                         watch_list_watched=False, 
                         watch_list_date=get_time(),
                         watch_list_user_email=get_user_email(),
                         watch_list_user_name=get_user_name(),
                         watch_list_rating=0,
                         watch_list_time_stamp=get_time(),
                         watch_list_review=''
                         )
    redirect(URL('index'))
    return 'Movie Quick Added'


# #######################################################
# Feed
# #######################################################
# TODO
# 1. Find a way to show only friends list's added movies with a timestamp similar to Twitter
@action('feed')
@action.uses(db, auth.user, 'feed.html')
def feed():
    movie_rows = db(db.watch_list.watch_list_user_email).select() # This gets all movie entries
    #movie_rows = db(db.watch_list).select() # This gets all movie entries
    user_rows = db(db.user.user_email).select() # All users
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

        # get comments for the post
        comment_rows = db(db.review_comment.watch_list_id == m['id']).select()
        # also get the pfps for each commentor
        for comment in comment_rows:
            user_row = db(db.user.user_email == comment['user_email']).select().first    ()
            thumbnail_link = user_row['user_thumbnail']
            if thumbnail_link == None:
                thumbnail_link == "https://www.jing.fm/clipimg/detail/195-1952632_account-customer-login-man-user-icon-login-icon.png"
            comment['thumbnail'] = thumbnail_link
        m['comments'] = comment_rows

        m['thumbnail'] = None

        for user in user_rows:
            if user['user_email'] == m['watch_list_user_email']:
                m['thumbnail'] = user['user_thumbnail']


    print(movie_rows)
    return dict(rows=movie_rows, url_signer=url_signer,
                add_movie_url = URL('add_movie', signer=url_signer),
                get_rating_url = URL('get_rating', signer=url_signer),
                set_rating_url = URL('set_rating', signer=url_signer),
                get_comment_url = URL('get_comment', signer=url_signer),
                get_comments_url = URL('get_comments', signer=url_signer),
                post_comment_url = URL('post_comment', signer=url_signer),
                user_email=get_user_email())


# #######################################################
# Notifications
# #######################################################
# TODO
# 1. Friend added/removed notification
# 2. Settings to show or not show friends added movies
@action('notifications')
@action.uses(db, auth.user, 'notifications.html')
def notifications():
    user = db(db.user.user_id == auth.current_user.get('id')).select()
    for u in user:
        id = u.id
        #print(u.id)
    rows = db(db.notifications.user_id == id).select()
    return dict(rows=rows, url_signer=url_signer)

#delete notification
@action('delete_notification/<notifications_id:int>')
@action.uses(db, auth.user, url_signer.verify())
def delete_notification(notifications_id=None):
    assert notifications_id is not None
    db(db.notifications.id == notifications_id).delete()
    #print("did I delete ?")
    redirect(URL('notifications'))


# #######################################################
# Profile
# #######################################################
# TODO
# 1. Find a way to display list of all friends
@action('profile')
@action.uses(db, auth.user, 'profile.html')
def profile():

    db.user.update_or_insert(user_name = auth.current_user.get('first_name') + " " + auth.current_user.get('last_name'),
                   user_email = get_user_email(),
                   user_id = auth.current_user.get('id'))
    follower_count = len(db(db.follower.reference == auth.current_user.get('id')).select().as_list())
    following_count = len(db(db.following.reference == auth.current_user.get('id')).select().as_list())

    return dict(load_user_url=URL('load_user', signer=url_signer),
                load_following_url=URL('load_following', signer=url_signer),
                load_follower_url=URL('load_follower', signer=url_signer),
                upload_thumbnail_url=URL('upload_thumbnail', signer=url_signer),
                search_url=URL('search_friends', signer=url_signer),
                add_following_url=URL('add_following', signer=url_signer),
                following_count=following_count,
                follower_count=follower_count)

#intialize user database in profile.js: load_user_url
@action('load_user')
@action.uses(db, auth.user, session, url_signer.verify())
def load_user():

    userrows = db((db.user.user_email == get_user_email())).select().as_list()

    return dict(userrows = userrows)

#intialize following database in profile.js: load_following_url
@action('load_following')
@action.uses(db, auth.user, session, url_signer.verify())
def load_following():

    followingrows = db(db.following.reference == auth.current_user.get('id')).select().as_list()

    return dict(followingrows = followingrows)

#intialize followerdatabase in profile.js: load_follower_url
@action('load_follower')
@action.uses(db, auth.user, session, url_signer.verify())
def load_follower():

    followerrows = db(db.follower.reference == auth.current_user.get('id')).select().as_list()

    return dict(followerrows = followerrows)

#sub-nav tags on profile page (for later if I have time)
"""
@action('following')
@action.uses(db, auth.user, 'following.html')
def profile():
    rows = db((db.user.user_email == get_user_email())).select()

    #followings = db(db.following.user_id == auth.current_user.get('id'))
    return dict(rows=rows)


@action('followers')
@action.uses(db, auth.user, 'followers.html')
def profile():
    rows = db((db.user.user_email == get_user_email())).select()


    # followings = db(db.following.user_id == auth.current_user.get('id'))
    return dict(rows=rows)
"""

#uoload thumbnail API
@action('upload_thumbnail', method="POST")
@action.uses(url_signer.verify(), db)
def upload_thumbnail():
    user_id = request.json.get("user_id")
    thumbnail = request.json.get("thumbnail")
    db(db.user.id == user_id).update(user_thumbnail =thumbnail)
    return "ok"

#search friends API
@action('search_friends')
@action.uses(db, auth)
def search_friends():

    q = request.params.get("q")
    rows = db(db.auth_user.email == q).select().as_list()
    results = rows

    #print(results)
    return dict(results = results)


# add people to your following list API
@action('add_following', method=["GET", "POST"])
@action.uses(db, auth.user, url_signer.verify())
def add_following():
    email = request.json.get("email")
    #print(email)
    assert email is not None
    rows = db(db.auth_user.email == email).select().as_list()
    #print(rows)
    followerthumbnail = None
    followingthumbnail = None

    getfollowerthumbnail = db(db.user.user_email == auth.current_user.get('email')).select().as_list()
    for t in getfollowerthumbnail:
        followerthumbnail = t['user_thumbnail']
    for r in rows:
        getfollowingthumbnail = db(db.user.user_email == r['email']).select().as_list()
        for t in getfollowingthumbnail:
            followingthumbnail = t['user_thumbnail']
            followingid = t['id']
        user = db(db.user.user_id == auth.current_user.get('id')).select()
        for u in user:
            id = u.id
        db.following.update_or_insert(following_id = r['id'],
                            following_user_name = r['first_name'] + " " + r['last_name'],
                            following_user_email = r['email'],
                            following_thumbnail = followingthumbnail,
                            reference = auth.current_user.get('id'))

        db.notifications.update_or_insert(user_id = id,
                                          message = "You are now following " + r['first_name'] + " " + r['last_name'] + "!")

        db.follower.update_or_insert(follower_id = auth.current_user.get('id'),
                                     follower_user_name = auth.current_user.get('first_name') + " " + auth.current_user.get('last_name'),
                                     follower_user_email = auth.current_user.get('email'),
                                     follower_thumbnail = followerthumbnail,
                                     reference = r['id'])
        db.notifications.update_or_insert(user_id = t['id'],
                                          message = auth.current_user.get('first_name') + " "
                                            + auth.current_user.get('last_name') + " "
                                            + "is now following you!")
    redirect(URL('profile'))
    return "ok"


# get an individual comment for a user given the movie listing id
# there's only one comment per user on a given movie listing id so this is ok
@action('get_comment')
@action.uses(db, auth.user, url_signer.verify())
def get_comment():
    watch_list_id = request.params.get('watch_list_id')
    row = db((db.review_comment.user_email == get_user_email()) &
             (db.review_comment.watch_list_id == watch_list_id)).select().first()
    comment = ""
    if row is not None:
        comment = row.comment
    return dict(comment=comment)

# get comments that are visible when you hover over the authors
# icon below your own review
@action('get_comments')
@action.uses(db, auth.user, url_signer.verify())
def get_comments():
    rows = db(db.review_comment).select()
    comments = {}
    # end result should be, as EX:
    #{1:{"name":"John","comment":"Bad opinion"},2:{"name":"Dave","comment":"eh"}}
    for row in rows:
        comments[str(row.id)] = {"name":row.user_name,"comment":row.comment}
        
    return dict(comments=comments)
    
# post a comment to the review_comment db table
@action('post_comment', method=['POST'])
@action.uses(db, auth.user, url_signer.verify())
def post_comment():
    comment = request.json.get('comment')
    watch_list_id = request.json.get('listing_id')
    if len(comment.strip()) > 0:
        exists = "false"
        row = db((db.review_comment.user_email == get_user_email()) &
                 (db.review_comment.watch_list_id == watch_list_id)).select().first()
        if row is not None:
            exists = "true"

        db.review_comment.update_or_insert(
            (db.review_comment.user_email == get_user_email()) &
            (db.review_comment.watch_list_id == watch_list_id),
            watch_list_id=watch_list_id,
            comment=comment)
        return dict(stat="ok",updated=exists)
    else:
        return dict(stat="error")
