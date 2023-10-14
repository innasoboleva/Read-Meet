<h1 align="center">Read & Meet</h1>


## About The Project
Introducing **Read&Meet**: Your Gateway to One-Time Book Club! **Read&Meet** is an app designed to empower book enthusiasts to connect, engage, and discuss their favorite books by scheduling meeting in preson or online. 

### Here's what you can do with BookMeet:
1. _User:_<br>
Create new user and log in to be able to use this app fully!
2. _Book Discussion Meetings:_<br>
Create and host book discussion meetings centered around your favorite books.
Choose the date, time, and location for your meeting, record a video note for inviting more guests.
3. _Meeting Discovery:_<br>
Browse a diverse range of upcoming book discussion meetings created by fellow users for each possible book.
4. _Book Selection:_<br>
Select your preferred choice of book for your meeting from an extensive library of titles.
5. _Check reviews:_<br>
Take a look at what people are saying about each book right here on web-app.
6. _Discussions:_<br>
Engage in lively discussions with participants about the chosen book.
7. _Community Building:_<br>
Connect with like-minded individuals who share your passion for reading and book discussions.
8. _Seamless User Experience:_<br>
Enjoy a user-friendly interface that makes creating and managing meetings a breeze.

Experience the joy of discussing your favorite books with others who share your enthusiasm. With **Read&Meet**, every book discussion becomes an opportunity for insightful conversations, new friendships, and unforgettable reading experiences. Join us today and let the world of books come alive like never before!

### Project Tech Stack
Python, JavaScript, HTML5, CSS3, Flask, SQLAlchemy,  PostgreSQL, AJAX, Jinja2, React, Bootstrap, JSON, Pytest

### APIs Used
Google Books API, Yelp API, MediaStream API, Selenium, AWS SDK

### Data Model
**Reed&Meet** is using a PostgreSQL database and SQLAlchemy as an ORM.
![ Detailed data model](https://readmeet-video.s3.us-east-2.amazonaws.com/Data_model.png)

## Features
On the main page I implemented bootstrap carousel featuring popular books. This information was scraped from blog on GoodReads.
Also I've implemented sign in and sign up methods.
![ Sign in form](https://readmeet-video.s3.us-east-2.amazonaws.com/sign_in.png)

I integrated Google books api for book search. List of results is shown after processing JSON response.
![ List of books after search](https://readmeet-video.s3.us-east-2.amazonaws.com/search.png)

After selecting a book, a request is sent for fetching reviews from Goodreads using Selenium framework.
I created a form where users can schedule new meetings. 
![ Meeting form and reviews from Goodreads on book details page](https://readmeet-video.s3.us-east-2.amazonaws.com/book_details.png)

For meeting in person address is required. I integrated Yelp API to help search for a place.
![ Meeting form with option to search for place on Yelp](https://readmeet-video.s3.us-east-2.amazonaws.com/yelp.png)

I implemented a Video Recorder using the MediaStream API for creating video notes.
Before submission video is available for review or re-recording.
![ Meeting form with option to record video note](https://readmeet-video.s3.us-east-2.amazonaws.com/video.png)

Different react components on the main page are interconnected and display meetings that users can join, drop from or cancel if already created.
They are dynamically updated upon receiving JSON success response from server.
I implemented security methods to ensure that users won’t join same meetings twice.
![ Main page with React components](https://readmeet-video.s3.us-east-2.amazonaws.com/react.png)

Video note is also available for streaming here.


Notifications are displayed on top of the screen. 
Each message is independent and has its own timer set for 15sec.
![ Notifications for users ](https://readmeet-video.s3.us-east-2.amazonaws.com/messages.png)

### Show Your Support
Please, :+1: or :star: if it was helpful.
