# Movie Creep Usage
Movie Creep is an app that allows users to create a profile to track shows/movies they watch and share with others with ease. 

After watching a movie the user can add it to their movies watch list, or if they have not watched a movie they can add it to their planned movies. They can also add a review of the movie, along with which source they used to watch the movie. This is a social app, friends can add each other and examine others profiles and see what movies they have previously watched and their reviews of the movies on a main feed. There will also be a page for notifications, where users can see who has added them as a friend. Users can manually find movie recommendations based on authentic, trusted reviews from their friends. There will be a specific page for recommendations, which will show the user’s watched movies in order of most recommended. 

## Core Functionality

### Movie Watch List
This page serves as the home page for users as it consists of all the movies a user has added to track movies they have watched or to add movies they plan to watch. At first, the page appears blank, with only a button to 'Add New Movie'. Once clicked, the user is taken to a form asking for information about the movie the user is trying to add. The fields include Movie Title, Watched, Watch List Date, Your Movie Review, and Watch List Count. After submission, the page is reloaded to the original Movie Watch List, with the addition of the movie the user just added. Using the inputted movie title, the film's poster is accessed from a large database of movies we have used, and displayed to clearly represent the user's movie. Along with the image, the movie's title is shown. Every movie entry has a information symbol that can be found under the movie's title. When hovered over, this symbol opens a small screen with the Rating, Release Date, Runtime, Genre, and Plot of the movie. Many people watch the same movie multiple times. To track this activity, there is a counter that can be used to increment or decrement the number of times a user has watched the movie. The user also has the option to Like or Dislike the movie using interactive thumbs. Each user's entered review is displayed along with each movie. These movie entries automatically show up on the user's followers feeds, where they can add comments. All follower comments are represented by their respective follower's profile picture, which can be hovered on to see the actual comment. Every movie entry also consists of, an edit button to update any information using the add new movie form, and a delete button to delete the movie entry all together.

![screencapture-127-0-0-1-8000-MovieCreep-main-index-2021-06-07-17_27_26](https://user-images.githubusercontent.com/26385958/121103965-df0b4d80-c7b5-11eb-84e6-40d7fbb9d7e1.png)


### Feed
The feed page is where you can see what you and other people have added to their movie watch lists. On this page you'll be able to leave comments on other people's movie reviews. All of the user's followers who have left a comment will be visible to you so you will be able to see everyone's comment by hovering over their profile picture. You can leave a comment by clicking on the yellow comment button. This will open up a text box on that movie listing for you to type your comment into. When you are done, the post button is used to post the comment for others to see. The page will reload if you have not left a comment before but it will update without reloading any time after that. We have to autoreload on first comment because the profile pictures in the friends comment section are generated statically. It has to be there in order to hover over it and see the comment so we have to reload the page. If you are updating your comment then you will be able to see your old comment when you open up the comment text box again. You are only allowed one comment per user's movie listing so the old comment you had gets updated when you hit post. In this case, no autoreload happens because your profile picture was already there on the post. Hovering over it will show the updated comment.

<img width="1272" alt="Screen Shot 2021-06-07 at 5 34 52 PM" src="https://user-images.githubusercontent.com/26385958/121104367-c51e3a80-c7b6-11eb-9f0b-70dd0f330c8f.png">


### Profiles and Followers
The 'Profile' page is where users can make their accounts more personal. Users can upload an image to use as their profile picture, which will be used on all the user's movie entries and comments. This image can be changed at any time by first deleting the current image with the 'x' seen on the bottom left of the image, and then by reuploading a new image. The user's total number of movies watched, people they are following, and followers are all displayed at the top of this page to allow the user to keep tabs on their account. These numbers will constantly update as more movies are added to the watch list and more friends are added. In order to start connecting with friends, users can input friend's emails into the 'Add Friends' box on this page. If there is an account associated with the email, the friend's name will pop up with an add button that can be clicked to successfully follow them. As mentioned, users can follow people and also be followed. When a friend goes through this same process to add the user, the user will get a notification in the notifications tab informing them that they have a new follower. On the top right. ofthe profile page, there are a few buttons that allow the user to separate the information they see on the page by their movie watch list, following, or followers.

### Movie Recommendations
The Movie Recommendations page displays recommended movies based on the user's currently added movies, and what other Movie Creep users have watched or added to their profile. With the upper left buttons, the user can narrow down what kind of recommendations they want to see dynamically, and with the quick add button users can quickly add movies they are interested in to their watch list. 

## Getting Started
1. Sign up and sign into Movie Creep

2. Add movies you have seen or plan to in the Movie Watch List Tab

3. Follow your friends with their email in the profile page

4. View the feed to Creep on what your friends are watching

5. Check out the movie recommendations page to get similar suggestions of what to watch based on your profile and what your friends have watched



