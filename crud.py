""" CRUD operations. """
from models import db, User, Meeting, Book, List, connect_to_db

# Meetings
def get_all_meetings():
    """ Returns list of all meetings. """
    return Meeting.query.all()

def get_meeting_by_id(id):
    """ Returns meeting instance. """
    return Meeting.query.get(id)

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

# Lists
def get_list_by_id(id):
    """ Returns user's list by list id. """
    return List.query.get(id)

# Books
def get_books_in_list(list_id):
    """ Returns list of books in user's list. """
    list_of_books = List.query.get(list_id)
    return list_of_books.books

def get_book_by_id(isbn):
    """ Returns book. """
    return Book.query.get(isbn)



