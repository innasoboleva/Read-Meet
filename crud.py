""" CRUD operations. """
from models import db, User, Meeting, Book, List
from datetime import datetime
import pytz
from apis import *
from sqlalchemy import not_

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
            return {"status": "error", "message": "Can't find user as a guest in this meeting" }
    else:
        return {"status": "error", "message": "Can't find meeting or user data" }
    

def update_past_meetings():
    all_meetings = Meeting.query.all()
    today = datetime.now(pytz.UTC)
    for meeting in all_meetings:
        if meeting.active == True:
            if meeting.day < today:
                meeting.active = False

# Users
def get_host_active_meetings(user_id):
    """ Returns all meetings that user created as a host and that will be in the future. """
    user = User.query.get(user_id)
    active_host_meetings = [meeting for meeting in user.host_meetings if meeting.active]
    return active_host_meetings


def get_guest_active_meetings(user_id):
    """ Returns all meetings that user joined as a guest. """
    user = User.query.get(user_id)
    active_guest_meetings = [meeting for meeting in user.guest_meetings if meeting.active]
    return active_guest_meetings


def get_user_by_id(id):
    """ Returns user instance. """
    return User.query.get(id)


def does_user_exist(email):
    """ Returns True, if email is already in a database. """
    user_to_check = User.query.filter(User.email == email).first()
    return bool(user_to_check)


def get_user_by_email(email):
    """ Returns user, if exists. """
    return User.query.filter(User.email == email).first()


# Books
def get_book_by_id(book_id):
    """ Returns book. """
    return Book.query.get(book_id)

def get_popular_books():
    """ Returns list of popular books. """
    day = datetime.today().strftime("%Y-%m")
    return Book.query.filter(Book.popular_book == day).all()


def add_new_popular_books_to_db():
    """
    Function for checking new books, once every new month and to seed db with popular books for current month.
    """
    popular_books = goodreads_api.get_books_for_carousel()
    status = popular_books.get("status")
    if status == "success":
        list_of_titles = popular_books.get("titles")
        for book in list_of_titles:
            result_from_book_search = books_api.find_popular_book(book)
            book_status = result_from_book_search.get("status")
            if book_status == "success":
                books = result_from_book_search.get("books")
                if books:
                    popular_book = books[0]
                    book_id = popular_book.get("book_id")
                    title = popular_book.get("title")
                    subtitle = popular_book.get("subtitle")
                    authors = popular_book.get("authors")
                    description = popular_book.get("description")
                    books_ISBN = popular_book.get("ISBN")
                    image = popular_book.get("image_url")
                    popular_book = datetime.today().strftime("%Y-%m")
                    new_book = Book.create(book_id=book_id, isbn=books_ISBN, title=title, subtitle=subtitle, authors=authors, \
                    image_url=image, description=description, popular_book=popular_book)
                    db.session.add(new_book)

    db.session.commit()


def delete_old_unused_books_from_db():
    """ Function for deleting old unused book from Database """
    current_day = datetime.today().strftime("%Y-%m")
    subquery = db.session.query(Meeting.book_id).distinct()

    db.session.query(Book).filter(not_(Book.book_id.in_(subquery))).\
        filter(Book.popular_book != current_day).\
        filter(Book.popular_book.isnot(None)).\
            delete(synchronize_session=False)
    
    db.session.commit()


# Lists
