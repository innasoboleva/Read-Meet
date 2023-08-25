import os
from apis import books_api, yelp_api, goodreads_api
from flask import Flask, render_template, jsonify, request, session
from models import connect_to_db , db, User
import crud


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_KEY')


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")


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


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='localhost') # localhost preferable for video api
    