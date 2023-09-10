import os
from apis import books_api, yelp_api, goodreads_api
from flask import Flask, render_template, jsonify, request, session, flash
from models import connect_to_db , db, User, Meeting, Book
import crud
from datetime import datetime


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_KEY')


@app.route("/")
def homepage():
    """Show homepage."""
    print("Index: ", session.get('user_id'))
    return render_template("index.html")


@app.route("/books")
def show_books_page():
    """Show page with rendered books."""
    print("Books user: ", session.get('user_id'))
    return render_template("index.html")


@app.route("/api/get_books")
def get_books():
    """ Get books information with provided parameters. """
    search_req = request.args.get("search", None)
    page = request.args.get("page")
    result = books_api.find_list_of_books(search_req, int(page) if page else 0)
    return jsonify(result)



@app.route("/api/create_new_user", methods=["POST"])
def create_new_user():
    """ If user's email is not present in DB, creates new user and returns status success. If exists, returns error."""
    json_data = request.get_json()
    email = json_data.get("user_email")
    if crud.does_user_exist(email):
        return jsonify({ "status": "error", "message": f"User with email {email} already exists. Please try again."})
    else:
        name = json_data.get("user_name")
        address = json_data.get("user_address", None)
        zipcode = json_data.get("user_zipcode", None)
        age = json_data.get("user_age", None)
        password = json_data.get("user_password")
        if address == "":
            address = None
        if age == "":
            age = None
        else:
            age = int(age)
        try:
            new_user = User.create(email, password, name, zipcode, address, age)
            db.session.add(new_user)
            db.session.commit()
            flash("New user successfully created.")
            session["user_id"] = new_user.user_id
            session["name"] = name
            if address:
                session["address"] = address
            if zipcode:
                session["zipcode"] = zipcode
            flash(f"You logged in with {email}!")
        except:
            return jsonify({ "status": "error", "message": "There was a server problem. Please try again..."})
        return jsonify({ "status": "success", "new_user": \
                        { "user_id": new_user.user_id, "name": name, "address": address, "zipcode": zipcode } })


@app.route("/api/get_current_user")
def get_current_user():
    """ Get current user information if loged in."""
    user = session.get("user_id", None)
    name = session.get("name", None)
    address = session.get("address", None)
    zipcode = session.get("zipcode", None)
    return jsonify({"user_id": user, "name": name, "address": address, "zipcode": zipcode })


@app.route("/api/login_user", methods=["POST"])
def login():
    """ Check if user exists in DB, add to session if he is. Returns status. 
        Assums that email and password are not empty.
    """
    json_data = request.get_json()
    email = json_data.get("user_email")
    password = json_data.get("user_password")
    user = crud.get_user_by_email(email)
    if user:
        if user.password == password:
            session["user_id"] = user.user_id
            session["name"] = user.name
            session["zipcode"] = user.zipcode
            if user.address is not None:
                session["address"] = user.address
            flash(f"You successfully logged in with {email}!")
            print(f"You successfully logged in with {email}!")
            print ({ "user_id": user.user_id, "name": user.name, "address": user.address, "zipcode": user.zipcode })
            return jsonify({ "status": "success", \
                            "user": { "user_id": user.user_id, "name": user.name, "address": user.address, "zipcode": user.zipcode } })
        else:
            print("Wrong password")
            return jsonify({ "status": "error", "message": "Wrong password. Please try again..."})
    else:
        print("No user")
        return jsonify({ "status": "error", "message": "There is no user with this email. Please try again..."})
    

@app.route("/api/logout_user")
def logout():
    """ Delets user from session. Returns status. 
        Assums that user is not empty.
    """
    if "user_id" in session:
        session["user_id"] = None
        session["name"] = None
        session["zipcode"] = None
        if "address" in session:
            session["address"] = None
        flash("You logged out!")
        print("Session, log out, user_id: ", session.get("user_id"))
        return jsonify({ "status": "success" })
    else:
        print("logged out: status: error")
        return jsonify({ "status": "error", "message": "Could not log out, server is not responding."})
    

@app.route("/api/get_all_meetings")
def get_all_active_meetings_data():
    """ Get all data from database for all meetings. """
    meeting_list_of_dict = []
    all_meetings = crud.get_all_active_meetings()
    if all_meetings:
        for meeting in all_meetings:
            meeting_dict = meeting.to_dict()
            list_of_guests = [guest.user_id for guest in meeting.attending_guests]
            meeting_dict["guests_count"] = len(meeting.attending_guests)
            meeting_dict["guests"] = list_of_guests
            meeting_list_of_dict.append(meeting_dict)
    return jsonify(meeting_list_of_dict)


@app.route("/api/get_user_by_id", methods=["POST"])
def get_user_by_id():
    """ Get user info by id. """
    user_id = request.get_json().get("host_id")
    if user_id:
        user = crud.get_user_by_id(user_id)
        return jsonify(user.to_dict())
    else:
        return {}
    

@app.route("/api/get_book_by_id", methods=["POST"])
def get_book_by_id():
    """ Get book data by id. """
    book_id = request.get_json().get("book_id")
    if book_id:
        book = crud.get_book_by_id(book_id)
        return jsonify(book.to_dict())
    else:
        return {}
    
@app.route("/api/get_all_meetings_for_book", methods=["POST"])
def get_meetings_for_book():
    """ Returns all meeting data for a book with requested id. """
    data = request.get_json()
    book_id = data.get("book_id")
    if book_id:
        meetings = crud.get_all_meetings_for_book(book_id)
        meeting_list_of_dict = []
        if meetings:
            for meeting in meetings:
                meeting_dict = meeting.to_dict()
                list_of_guests = [guest.user_id for guest in meeting.attending_guests]
                meeting_dict["guests_count"] = len(meeting.attending_guests)
                meeting_dict["guests"] = list_of_guests
                meeting_list_of_dict.append(meeting_dict)
        return jsonify({ "status": "success", "meetings": meeting_list_of_dict})
    else: 
        return jsonify({ "status": "error", "message": f"Couldn't get any meetings data for {book_id}."})
    

@app.route("/api/join_meeting", methods=["POST"])
def join_meeting():
    """ Sends request to db to join meeting. """
    data = request.get_json()
    user_id = data.get("user_id")
    meeting_id = data.get("meeting_id")
    meeting = crud.get_meeting_by_id(meeting_id)
    print(user_id, " joins", meeting_id)
    if (meeting and (len(meeting.attending_guests) != meeting.max_guests) and (meeting.host_id != user_id)):
        message = crud.join_meeting(user_id, meeting_id)
        if message['status'] == 'success':
            db.session.commit()
        flash(message['message'])
        print(message['message'])
        return jsonify(message)
    else:
        return jsonify({"status": "error", "message": "Can't find meeting or user data." })
    


@app.route("/api/drop_meeting", methods=["POST"])
def drop_meeting():
    """ Sends request to db to drop from meeting. """
    data = request.get_json()
    user_id = data.get("user_id")
    meeting_id = data.get("meeting_id")
    message = crud.drop_meeting(user_id, meeting_id)
    print(user_id, " drops", meeting_id)
    print(message)
    db.session.commit()
    flash(message['message'])
    return jsonify(message)


@app.route("/api/get_reviews_for_book", methods=["POST"])
def get_reviews_for_book():
    data = request.get_json()
    book_id = data.get("book_id")
    print("BOOK ", book_id)
    result = goodreads_api.get_reviews(book_id)
    print(result)
    return jsonify(result)


@app.route("/api/get_popular_books")
def get_popular_books():
    """ Returns list of popular books for previous month. """
    books = crud.get_popular_books()
    result = [book.to_dict() for book in books]
    return jsonify(result)


@app.route("/api/create_meeting", methods=["POST"])
def create_meeting():
    """ Creates new meeting and returns data as JSON. """
    data = request.get_json()
    book_id = data.get("book_id")
    print("Book_id", book_id)
    user_id = data.get("user_id")
    print("User_id: ", user_id)
    inputs = data.get("inputs")
    raw_day = inputs.get('day')
    day = datetime.fromisoformat(raw_day)
    raw_offline = inputs.get('offline')
    offline = True # check for zoom meeting or in person (offline) meeting
    if raw_offline != "offline":
        offline = False
    language = inputs.get('language', None)
    place = inputs.get('place')
    max_guests = inputs.get('max_guests')
    overview = inputs.get('overview', None)
    
    host = crud.get_user_by_id(user_id)
    book = crud.get_book_by_id(book_id)
    new_meeting = None
   
    # if book is not in a DB
    if book is None:
        new_book_response = books_api.find_book(book_id)
        print("Book response", new_book_response)
        if new_book_response.get("status") == "success":
            print("Creating new book...")
            book = new_book_response['book']
            isbn = book.get('ISBN')
            title = book.get('title')
            subtitle = book.get('subtitle')
            image_url = book.get('image_url')
            description = book.get('description')
            authors = book.get('authors')
            if isbn:
                new_book = Book.create(isbn, title, authors, subtitle, \
                                       image_url=image_url, description=description) # isbn, title, authors, subtitle=None, popular_book=None, image_url=None, description=None
                print(new_book)
                db.session.add(new_book)
                new_meeting = Meeting.create(new_book, day, offline, host, max_guests, overview=overview, place=place, language=language)
                db.session.add(new_meeting)
    else:
        new_meeting = Meeting.create(book, day, offline, host, max_guests, overview=overview, place=place, language=language)
        print(new_meeting)
        db.session.add(new_meeting)
    
    db.session.commit()
    
    if new_meeting:
        meeting_dict = new_meeting.to_dict()
        list_of_guests = [guest.user_id for guest in new_meeting.attending_guests]
        meeting_dict["guests_count"] = len(new_meeting.attending_guests)
        meeting_dict["guests"] = list_of_guests
        print(meeting_dict)
        return jsonify({ "status": "success", "new_meeting": meeting_dict })
    else:
        return jsonify({"status": "error", "message": "Couldn't create new meeting, server error" })


@app.route("/api/get_yelp_places", methods=["POST"])
def get_yelp_businesses():
    data = request.get_json()
    term = data.get("place")
    page = data.get("page", 0)
    zipcode = session.get("zipcode")
    if zipcode:
        data = yelp_api.find_places(zipcode, term, page)
        return jsonify(data)
    else:
        print("error")
        return jsonify({ "status": "error", "message": "User is not logged in!"})


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='127.0.0.1') # localhost preferable for video api
    