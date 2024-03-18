from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime
import re
from sqlalchemy.dialects.postgresql import TIMESTAMP

db = SQLAlchemy()


class User(db.Model):
    """ A user. """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True, server_default=text("nextval('user_id_seq')"))
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    zipcode = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    age = db.Column(db.Integer)

    host_meetings = db.relationship("Meeting", back_populates="host")
    lists = db.relationship("List", back_populates="user")
    guest_meetings = db.relationship("Meeting", secondary="guests", back_populates="attending_guests")

    @classmethod
    def create(cls, email, password, name, zipcode, address=None, age=None):
       """ Create and return a new user. """
       return cls(email=email, password=password, name=name, zipcode=zipcode, address=address, age=age)
    
    def to_dict(self):
        """ Returns dict with instance data. """
        return { "id": self.user_id, "email": self.email, "name": self.name, \
                "address": self.address, "zipcode": self.zipcode, "age": self.age }

    def __repr__(self):
        return f'<User id={self.user_id} email={self.email} zipcode={self.zipcode}>'
    
    
class Book(db.Model):
    """ A book. """

    __tablename__ = "books"

    book_id = db.Column(db.String, primary_key=True)
    ISBN = db.Column(db.String)
    title = db.Column(db.String, nullable=False)
    subtitle = db.Column(db.String)
    authors = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String)
    popular_book = db.Column(db.String)

    meetings = db.relationship("Meeting", back_populates="book")
    lists = db.relationship("List", secondary="books_lists", back_populates="books")

    @classmethod
    def create(cls, book_id, isbn, title, authors, subtitle=None, popular_book=None, image_url=None, description=None):
       """ Create and return a new book. """
       return cls(book_id=book_id, ISBN=isbn, title=title, subtitle=subtitle, authors=authors, \
                  image_url=image_url, description=description, popular_book=popular_book)
    
    def to_dict(self):
        """ Returns dict with instance data. """
        return { "book_id": self.book_id, "ISBN": self.ISBN, "title": self.title, "subtitle": self.subtitle, \
                "authors": self.authors, "description": self.description, "image_url": self.image_url }

    def __repr__(self):
        return f"<Book ISBN={self.ISBN} title={self.title} authors={self.authors}>"
    

class Meeting(db.Model):
    """ A meeting. """

    __tablename__ = "meetings"

    meeting_id = db.Column(db.Integer, autoincrement=True, primary_key=True, server_default=text("nextval('meeting_id_seq')"))
    book_id = db.Column(db.String, db.ForeignKey("books.book_id"), nullable=False)
    day = db.Column(TIMESTAMP(timezone=True), nullable=False)
    place = db.Column(db.String)
    address = db.Column(db.String)
    offline = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    language = db.Column(db.String, nullable=False)
    video_note = db.Column(db.String)
    overview = db.Column(db.Text)
    host_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)

    book = db.relationship("Book", back_populates="meetings")
    host = db.relationship("User", back_populates="host_meetings")
    attending_guests = db.relationship("User", secondary="guests", back_populates="guest_meetings")

    @classmethod
    def create(cls, book, day, offline, host, max_guests, video_note=None, overview=None, place=None, address=None, language="EN"):
       """ Create and return a new meeting instance. """
       return cls(book=book, day=day, place=place, address=address, host=host, \
                  offline=offline, max_guests=max_guests, active=True, language=language, video_note=video_note, overview=overview)
    
    def to_dict(self):
        """ Returns data of an instance in a dictionary. """
        meeting_date = str(self.day)

        return { "id": self.meeting_id, "book_id": self.book_id, "book_title": self.book.title, \
                "book_authors": self.book.authors, "date": meeting_date, \
                "place": self.place, "address": self.address, "offline": self.offline, \
                    "language": self.language, "video": self.video_note, \
                        "overview": self.overview, "host_id": self.host_id, "max_guests": self.max_guests, "host_name": self.host.name }

    def __repr__(self):
        return f"<Meeting id={self.meeting_id} book={self.book} day={self.day} active={self.active}>"
    

class Guests(db.Model):
    """ Middle table for users and meetings. User can attend many meetings, meetings can have many guests (users). """
    
    __tablename__ = "guests"

    guest_id = db.Column(db.Integer, autoincrement=True, primary_key=True, server_default=text("nextval('guest_id_seq')"))
    meeting_id = db.Column(db.Integer, db.ForeignKey("meetings.meeting_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)


class List(db.Model):
    """ A list of books. """

    __tablename__ = "lists"

    list_id = db.Column(db.Integer, autoincrement=True, primary_key=True, server_default=text("nextval('list_id_seq')"))
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    user = db.relationship("User", back_populates="lists")
    books = db.relationship("Book", secondary="books_lists", back_populates="lists")

    @classmethod
    def create(cls, name, user):
       """ Create and return a new list. """

       return cls(name=name, user=user)

    def __repr__(self):
        return f"<List name={self.name} user={self.user_id}>"
    

class BookList(db.Model):
    """ Associate table for connecting lists and books, many-to-many relationship. """

    __tablename__ = "books_lists"

    booklist_id = db.Column(db.Integer, autoincrement=True, primary_key=True, server_default=text("nextval('booklist_id_seq')"))
    book_id = db.Column(db.String, db.ForeignKey("books.book_id"), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey("lists.list_id"), nullable=False)


def connect_to_db(flask_app, db_uri="postgresql:///readmeet", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)
    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)

# production block
from server import app
connect_to_db(app)