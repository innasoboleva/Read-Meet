from enum import Enum

class User:
    """
    Information about each unique user.
    """
    database =[] # temprorary holds emails
    id_count = 0

    def __init__(self, name, email, password, zipcode, address='',age=0):
        self.name = name
        self.email = email
        self.paaword = password
        self.zipcode = zipcode
        self.address = address
        self.age = age
        # pre-initialization of User object properties
        self.lists = []
        self.host_meetings = []
        self.guest_meetings = []
        # getting User's id, keeping track manually
        User.id_count += 1
        self.id = User.id_count

    @staticmethod
    def email_exists(email):
        if email in User.database:
            return True
        return False
    
    @staticmethod
    def add_email(email):
        User.database.append(email)


class Meeting:
    """
    Information about each meeting.
    """
    def __init__(self, host, book, date, time, place, language, offline=False):
        self.host = host
        self.book = book
        self.date = date
        self.time = time
        self.place = place
        self.language = language
        self.offline = offline
        # pre-initialization of Meeting object properties
        self.guests = []
        self.active = True


class List:
    """
    User's list to keep track of books.

    Consist of a single array of Books.
    """
    def __init___(self, name):
        self.name = name
        # pre-initialization of List object properties
        self.books = []


class Book:
    """
    Basic information about the book.
    """

    def __init__(self, title, author, description, avg_rating=0):
       self.author = author
       self.title = title
       self.description = description
       self.avg_rating = avg_rating


class Rating(Enum):
    ZERO_ = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
