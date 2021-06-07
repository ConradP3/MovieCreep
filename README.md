# MovieCreep
[![Platform: py4web](https://img.shields.io/badge/platform-py4web-informational.svg)](https://github.com/web2py/py4web)
## Purpose
Movie Creep is an app that allows users to create a profile to track shows/movies they watch and share with others with ease. 

<i>Complete documentation on usage of Movie Creep can be found in USAGE.md</i>

## Installation
1. Install and setup Py4web. (instructions: https://github.com/web2py/py4web)
2. Install requirements and Movie Creep
```
pip install -r requirements.txt
cd Py4web/apps
git clone https://github.com/ConradP3/MovieCreep.git
cd ../..
py4web run apps

```

Movie Creep will be available locally at : http://127.0.0.1:8000/MovieCreep


## Tabs
- /index 
    feed of users previously added movies, see user profile image/info. Includes already watched movies user has watched and movies user plans to watch. Search bar for movies.

- /Movie Recommendations
Most Watched movies at top, takes into account user's added movies and display what they may be interested in. Also recommends what other users have added to their profile.

- /Feed (Main feature)
    Friends/own activity for movies if signed in. Comments of other users is dispalyed.

- /Notifications (optional)
    friend requests, notify user of potential movies user is interested in.

- /Profile 
    User information, profile picture, friends list (following/followers), following/followers count, movies watched count

## User Flow
1. Home page 
- Main page has logo + basic information 
- Sign in button in right upper corner -> takes you to sign in page
- Sign-in
- Sign-up
- Forgot Password

--> After Successful Login
2. Go to Main Feed
- tweet format with a long list of movie reviews/”tweets” from users you follow
- Has functionality to like and comment on these tweets
- Top has an area to make a “tweet” and takes user to form to successfully see it on feed
- NavBar has list of all the tabs -> when signed in the top right corner changes to options of either signing out or going to personal profile
- Search tab to be able to get information about a specific movie?

3. Personal Profile
- Information about the user: 
    - User name
    - User email
    - Profile picture
- User can add, remove and change profile picture here
- Follower counts, Following counts, movies watched
- Movie watch List
- Ability to see other users profile's by clicking on their name

4. Movie Watch List
- This is a list of movies that either the user wants to watch or has watched
- Separate Lists into has watched and watched into this tab
- SUB TABS: Watched/To Watch
- Each has a list of movies, with all information about the movie
- This will be used to find possible recommendations based on common genres or actors in the movie
- In order to mark a movie as watched: 

5. Notifications
- Whenever a user follows another user or another user follows them, they will receive a notification in this tab
- Notifications can be deleted whenever the user clicks the "x" on the notification

6. Recommendations
- Base recommendations on movies watched by users followed
- Base recommendations on user’s movie list (similar content)
- List of movies based with all information (toggle different recommendations)

## Technologies
- Py4web
- Bulma CSS
- Vue.js

Recommendations
- Numpy
- Pandas
- Sklearn



## Data Sources
- [OMDBb API](http://omdbapi.com/) RESTful web service to obtain movie information, over 280,000 images
- [The Movies Dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset) Metadata for movies listed in the Full MovieLens Dataset. (Kaggle)




