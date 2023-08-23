from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """ A user. """

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
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

    def __repr__(self):
        return f'<User id={self.id} email={self.email} zipcode={self.zipcode}>'
    

class Meeting(db.Model):
    """ A meeting. """

    __tablename__ = "meetings"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book = db.Column(db.String, db.ForeignKey("books.ISBN"), nullable=False)
    day = db.Column(db.DateTime, nullable=False)
    place = db.Column(db.String)
    address = db.Column(db.String)
    offline = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    language = db.Column(db.String, nullable=False)
    video_note = db.Column(db.String)
    overview = db.Column(db.Text)
    host_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    host = db.relationship("User", back_populates="host_meetings", nullable=False)
    attending_guests = db.relationship("User", secondary="guests", back_populates="guest_meetings")

    @classmethod
    def create(cls, book, day, offline, host, video_note=None, overview=None, place=None, address=None, language="EN"):
       """ Create and return a new meeting instance. """
       return cls(book=book, day=day, place=place, address=address, host=host, \
                  offline=offline, active=True, language=language, video_note=video_note, overview=overview)

    def __repr__(self):
        return f"<Meeting id={self.id} book={self.book} day={self.day} active={self.active}>"
    

class Guests(db.Model):
    """ Middle table for users and meetings. User can attend many meetings, meetings can have many guests (users). """
    
    __tablename__ = "guests"

    meeting_id = db.Column(db.Integer, db.ForeignKey("meetings.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    

class Book(db.Model):
    """ A book. """

    __tablename__ = "books"

    ISBN = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    authors = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    book_url = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    popular_book = db.Column(db.Date)

    lists = db.relationship("List", secondary="books_lists", back_populates="books")

    @classmethod
    def create(cls, isbn, title, authors, book_url, image_url=None, description=None):
       """ Create and return a new book. """
       return cls(ISBN=isbn, title=title, authors=authors, book_url=book_url, image_url=image_url, description=description)

    def __repr__(self):
        return f"<Book ISBN={self.ISBN} title={self.title} authors={self.authors}>"
    

class List(db.Model):
    """ A list of books. """

    __tablename__ = "lists"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

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

    book_id = db.Column(db.String, db.ForeignKey("books.ISBN"), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey("lists.id"), nullable=False)


def connect_to_db(flask_app, db_uri="postgresql:///meetbookclub", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)
    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    # echo=False: not to print out every query it executes.
    connect_to_db(app)