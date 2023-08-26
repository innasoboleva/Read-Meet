import os
from apis import books_api, yelp_api, goodreads_api
from flask import Flask, render_template, jsonify, request, session, flash
from models import connect_to_db , db, User
import crud


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_KEY')


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")


@app.route("/login")
def show_login_page():
    """Show login page."""

    return render_template("login.html")


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
        try:
            new_user = User.create(email, password, name, zipcode, address, age)
            db.session.add(new_user)
            db.session.commit()
            flash(f"New user successfully created. You logged in with {email}!")
            session["user_id"] = new_user.user_id
            session["name"] = name
            if address:
                session["address"] = address
            if zipcode:
                session["zipcode"] = zipcode
            if age:
                session["age"] = age
        except:
            return jsonify({ "status": "error", "message": "There was a server problem. Please try again..."})
        return jsonify({ "status": "success" })


@app.route("/api/get_current_user")
def get_current_user():
    """ Get current user information if loged in."""
    user = session.get("user_id", None)
    name = session.get("name", None)
    address = session.get("address", None)
    zipcode = session.get("zipcode", None)
    return jsonify({"user_id": user, "name": name, "address": address, "zipcode": zipcode })


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
    

@app.route("/api/join_meeting", methods=["POST"])
def join_meeting():
    """ Sends request to db to join meeting. """
    user_id = request.get_json().get("user_id")
    meeting_id = request.get_json().get("meeting_id")
    message = crud.join_meeting(user_id, meeting_id)
    db.session.commit()
    return jsonify(message)


@app.route("/api/drop_meeting", methods=["POST"])
def drop_meeting():
    """ Sends request to db to drop from meeting. """
    user_id = request.get_json().get("user_id")
    meeting_id = request.get_json().get("meeting_id")
    message = crud.drop_meeting(user_id, meeting_id)
    db.session.commit()
    return jsonify(message)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='localhost') # localhost preferable for video api
    