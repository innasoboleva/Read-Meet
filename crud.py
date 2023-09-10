""" CRUD operations. """
from models import db, User, Meeting, Book, List
from datetime import datetime

# Meetings
def get_all_meetings():
    """ Returns list of all meetings. """
    return Meeting.query.all()

def get_all_active_meetings():
    """ Returns list of all ACTIVE meetings. """
    return Meeting.query.filter(Meeting.active == True).all()

def get_all_meetings_for_book(book_id):
    """ Returns list of all ACTIVE meetings for book with book_id. """
    return Meeting.query.filter(Meeting.active == True, Meeting.book_id == book_id).all()

def get_meeting_by_id(id):
    """ Returns meeting instance. """
    return Meeting.query.get(id)

def join_meeting(user_id, meeting_id):
    """ Adds user to meeting as a guest. """
    meeting = Meeting.query.get(meeting_id)
    user = User.query.get(user_id)
    if user and meeting:
        if user not in meeting.attending_guests and len(meeting.attending_guests) < meeting.max_guests:
            meeting.attending_guests.append(user)
        return {"status": "success", "message": f"{user.name} joined meeting for '{meeting.book.title}' successfully!"}
    else:
        return {"status": "error", "message": "Can't find meeting or user data" }

def drop_meeting(user_id, meeting_id):
    """ Removes user from meeting if he is a guest. """
    meeting = Meeting.query.get(meeting_id)
    user = User.query.get(user_id)
    if meeting and user:
        if user in meeting.attending_guests:
            meeting.attending_guests.remove(user)
            return {"status": "success", "message": f"{user.name} dropped from meeting for '{meeting.book.title}' successfully!" } 
    else:
        return {"status": "error", "message": "Can't find meeting or user data" }

# Users
def get_host_meetings(user_id):
    """ Returns all meetings that user created as a host. """
    user = User.query.get(user_id)
    return user.host_meetings

def get_guest_meetings(user_id):
    """ Returns all meetings that user joined as a guest. """
    user = User.query.get(user_id)
    return user.guest_meetings

def get_user_by_id(id):
    """ Returns user instance. """
    return User.query.get(id)

def get_user_lists(user_id):
    """ Returns user's lists of books. """
    user = User.query.get(user_id)
    return user.lists

def does_user_exist(email):
    """ Returns True, if email is already in a database. """
    user_to_check = User.query.filter(User.email == email).first()
    return bool(user_to_check)

def get_user_by_email(email):
    """ Returns user, if exists. """
    return User.query.filter(User.email == email).first()


# Lists
def get_list_by_id(id):
    """ Returns user's list by list id. """
    return List.query.get(id)

# Books
def get_books_in_list(list_id):
    """ Returns list of books in user's list. """
    list_of_books = List.query.get(list_id)
    return list_of_books.books

def get_book_by_id(book_id):
    """ Returns book. """
    return Book.query.get(book_id)

def get_popular_books():
    """ Returns list of popular books. """
    day = datetime.today().strftime("%Y-%m")
    return Book.query.filter(Book.popular_book == day).all()

def create_meeting(user_id, book_id, day, offline, max_guests, overview, place, language):
    """ Creates new meeting and returns it. """
    book = get_book_by_id(book_id)
    host = get_user_by_id(user_id)
    new_meeting = Meeting.create(book, day, offline, host, max_guests, overview=overview, place=place, language=language)
    return new_meeting
    # book, day, offline, host, max_guests, video_note=None, overview=None, place=None, address=None, language="EN"



