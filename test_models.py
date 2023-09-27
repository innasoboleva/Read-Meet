import os
import pytest
from models import db, User, Meeting, Book
from crud import *
from datetime import datetime, timedelta
import pytz


os.system('dropdb test_db')
os.system('createdb test_db')


@pytest.fixture
def test_app():
    print("Test app")
    from server import app
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///test_db" # separate test database
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = True

    db.app = app
    db.init_app(app)
    print("Connected to the db for TESTING!")
     
    with app.app_context():
        print("Create DB")
        db.create_all()  # Create the test database

    yield app

    with app.app_context():
        print("Drop DB")
        db.drop_all()  # Drop the test database
        db.session.close()


# @pytest.fixture
# def client(test_app):
#     return test_app.test_client()


def test_create_all(test_app):
    print("Checking user... test create all")
    new_user = User.create('test@example.com', '0000', 'Test Test', '94560', '304 Addison Ct., NY') #cls, email, password, name, zipcode, address=None, age=None):
    new_book = Book.create('1', '123', 'Title Test', 'Author test') #book_id, isbn, title, authors, subtitle=None, popular_book=None, image_url=None, description=None
    
    date_now = datetime.now() + timedelta(days=1) # adding one more day to now
    nyc = pytz.timezone('America/New_York')
    date_localized = nyc.localize(date_now)

    new_meeting = Meeting.create(new_book, date_localized, True, new_user, 10) #book, day, offline, host, max_guests, video_note=None, overview=None, place=None, address=None, language="EN"
    
    with test_app.app_context():
        db.session.add_all([new_user, new_book, new_meeting])
        db.session.commit()

    with test_app.app_context():
        user_from_db = User.query.filter_by(email='test@example.com').first()
        book_from_db = Book.query.filter_by(book_id='1').first()
        meeting_from_db = Meeting.query.filter_by(book_id='1').first()

    # Assert that the attributes match
    assert user_from_db is not None
    assert user_from_db.name == 'Test Test'
    assert user_from_db.email == 'test@example.com'
    assert user_from_db.password == '0000'
    assert user_from_db.zipcode == '94560'
    assert user_from_db.address == '304 Addison Ct., NY'

    assert book_from_db.book_id == '1'
    assert book_from_db.ISBN == '123'
    assert book_from_db.title == 'Title Test'
    assert book_from_db.authors == 'Author test'

    assert meeting_from_db.book_id == '1'
    assert meeting_from_db.day == date_localized
    assert meeting_from_db.offline == True
    assert meeting_from_db.host_id == user_from_db.user_id
    assert meeting_from_db.max_guests == 10


def test_meetings(test_app):
   
    new_user = User.create('test@example.com', '0000', 'Test Test', '94560', '304 Addison Ct., NY') #cls, email, password, name, zipcode, address=None, age=None):
    new_user2 = User.create('test2@example.com', '0001', 'Test 1', '94561', '305 Addison Ct., NY') #cls, email, password, name, zipcode, address=None, age=None):
    new_book = Book.create('1', '123', 'Title Test', 'Author test') #book_id, isbn, title, authors, subtitle=None, popular_book=None, image_url=None, description=None
    new_book2 = Book.create('2', '1234', 'Title Second Test', 'Author test') #book_id, isbn, title, authors, subtitle=None, popular_book=None, image_url=None, description=None
    
    # future
    date_now = datetime.now() + timedelta(days=1) # adding one more day to now
    nyc = pytz.timezone('America/New_York')
    date_localized = nyc.localize(date_now)
    # past
    date_localized2 = nyc.localize(datetime.now() + timedelta(days=-1))

    new_meeting = Meeting.create(new_book, date_localized, True, new_user, 10) #book, day, offline, host, max_guests, video_note=None, overview=None, place=None, address=None, language="EN"
    new_meeting2 = Meeting.create(new_book2, date_localized2, True, new_user2, 10) #book, day, offline, host, max_guests, video_note=None, overview=None, place=None, address=None, language="EN"
    
    with test_app.app_context():
        db.session.add_all([new_user, new_user2, new_book, new_book2, new_meeting, new_meeting2])
        new_meeting2.active = False
        db.session.commit()
   
    with test_app.app_context():
        all_meetings = get_all_meetings()
        all_active_meetings = get_all_active_meetings()
        meeting_for_book_1 = get_all_meetings_for_book('1') # for book_id
        meeting_for_book_2 = get_all_meetings_for_book('2') # for book_id
        
    assert isinstance(all_meetings, list)
    assert len(all_meetings) == 2

    for meeting in all_meetings:
        assert isinstance(meeting, Meeting)

    for meeting in all_meetings:
        assert hasattr(meeting, 'book_id')
        assert hasattr(meeting, 'host_id')
        assert hasattr(meeting, 'day')
        assert hasattr(meeting, 'offline')
        assert hasattr(meeting, 'max_guests')

    assert isinstance(all_active_meetings, list)
    assert len(all_active_meetings) == 1

    for meeting in all_active_meetings:
        assert isinstance(meeting, Meeting)


    assert isinstance(meeting_for_book_1, list)
    assert len(meeting_for_book_1) == 1

    for meeting in meeting_for_book_1:
        assert isinstance(meeting, Meeting)

    assert isinstance(meeting_for_book_1, list)
    assert len(meeting_for_book_2) == 0

    
def test_meeting_id_join(test_app):

    new_user = User.create('test@example.com', '0000', 'Test Test', '94560', '304 Addison Ct., NY') #cls, email, password, name, zipcode, address=None, age=None):
    new_user2 = User.create('test2@example.com', '0001', 'Test 1', '94561', '305 Addison Ct., NY') #cls, email, password, name, zipcode, address=None, age=None):
    new_book = Book.create('1', '123', 'Title Test', 'Author test') #book_id, isbn, title, authors, subtitle=None, popular_book=None, image_url=None, description=None
    new_book2 = Book.create('2', '1234', 'Title Second Test', 'Author test') #book_id, isbn, title, authors, subtitle=None, popular_book=None, image_url=None, description=None
    
    # future
    date_now = datetime.now() + timedelta(days=1) # adding one more day to now
    nyc = pytz.timezone('America/New_York')
    date_localized = nyc.localize(date_now)
    # past
    date_localized2 = nyc.localize(datetime.now() + timedelta(days=-1))

    new_meeting = Meeting.create(new_book, date_localized, True, new_user, 10) #book, day, offline, host, max_guests, video_note=None, overview=None, place=None, address=None, language="EN"
    new_meeting2 = Meeting.create(new_book2, date_localized2, True, new_user2, 10) #book, day, offline, host, max_guests, video_note=None, overview=None, place=None, address=None, language="EN"
    
    with test_app.app_context():
        db.session.add_all([new_user, new_user2, new_book, new_book2, new_meeting, new_meeting2])
        new_meeting2.active = False
        db.session.commit()

        some_meeting = Meeting.query.first()
        some_user = get_user_by_id('2')
    
        assert get_meeting_by_id(some_meeting.meeting_id) == some_meeting
        assert join_meeting(some_user.user_id, some_meeting.meeting_id) == {"status": "success", "message": f"{some_user.name} joined meeting for '{some_meeting.book.title}' successfully!"}
        db.session.commit()

        assert join_meeting("300", some_meeting.meeting_id) == {"status": "error", "message": "Can't find meeting or user data" }
        assert join_meeting(some_user.user_id, "900") == {"status": "error", "message": "Can't find meeting or user data" }

        assert drop_meeting(some_user.user_id, some_meeting.meeting_id) == {"status": "success", "message": f"{some_user.name} dropped from meeting for '{some_meeting.book.title}' successfully!" }
        db.session.commit()

        assert drop_meeting("200", some_meeting.meeting_id) == {"status": "error", "message": "Can't find meeting or user data" }
        assert drop_meeting(some_user.user_id, "500") == {"status": "error", "message": "Can't find meeting or user data" }


def test_update_past_meetings(test_app):
    new_user = User.create('test@example.com', '0000', 'Test Test', '94560', '304 Addison Ct., NY') #cls, email, password, name, zipcode, address=None, age=None):
    new_user2 = User.create('test2@example.com', '0001', 'Test 1', '94561', '305 Addison Ct., NY') #cls, email, password, name, zipcode, address=None, age=None):
   
    new_book = Book.create('1', '123', 'Title Test', 'Author test') #book_id, isbn, title, authors, subtitle=None, popular_book=None, image_url=None, description=None
    new_book2 = Book.create('2', '1234', 'Title Second Test', 'Author test') #book_id, isbn, title, authors, subtitle=None, popular_book=None, image_url=None, description=None
    
    # future
    date_now = datetime.now() + timedelta(days=1) # adding one more day to now
    nyc = pytz.timezone('America/New_York')
    date_localized = nyc.localize(date_now)
    # past
    date_localized2 = nyc.localize(datetime.now() + timedelta(days=-1))

    new_meeting = Meeting.create(new_book, date_localized, True, new_user, 10) #book, day, offline, host, max_guests, video_note=None, overview=None, place=None, address=None, language="EN"
    new_meeting2 = Meeting.create(new_book2, date_localized2, True, new_user2, 10) #book, day, offline, host, max_guests, video_note=None, overview=None, place=None, address=None, language="EN"
    
    with test_app.app_context():
        db.session.add_all([new_user, new_user2, new_book, new_book2, new_meeting, new_meeting2])
        db.session.commit()

        some_meeting = Meeting.query.filter_by(book_id='2').first()

        assert some_meeting.active == True

        update_past_meetings()
        db.session.commit()
        updated_meeting = Meeting.query.filter_by(book_id='2').first()

        assert updated_meeting.active == False


def test_get_active_meetings(test_app):
    pass


def test_user_exist_check_by_email(test_app):
    pass

"""


# Users
def get_host_active_meetings(user_id):
   
    user = User.query.get(user_id)
    active_host_meetings = [meeting for meeting in user.host_meetings if meeting.active]
    return active_host_meetings


def get_guest_active_meetings(user_id):
   
    user = User.query.get(user_id)
    active_guest_meetings = [meeting for meeting in user.guest_meetings if meeting.active]
    return active_guest_meetings


def does_user_exist(email):
   
    user_to_check = User.query.filter(User.email == email).first()
    return bool(user_to_check)


def get_user_by_email(email):
    
    return User.query.filter(User.email == email).first()


# Books
def get_book_by_id(book_id):
    
    return Book.query.get(book_id)

def get_popular_books():
    
    day = datetime.today().strftime("%Y-%m")
    return Book.query.filter(Book.popular_book == day).all()

def create_meeting(user_id, book_id, day, offline, max_guests, overview, place, language):
   
    book = get_book_by_id(book_id)
    host = get_user_by_id(user_id)
    new_meeting = Meeting.create(book, day, offline, host, max_guests, overview=overview, place=place, language=language)
    return new_meeting



"""