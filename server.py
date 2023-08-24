import os
from apis import books_api, yelp_api, goodreads_api
from flask import Flask, render_template, jsonify
from models import connect_to_db , db, User
import crud


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_KEY')


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")

@app.route("/api/get_all_meetings")
def get_all_meetings_data():
    """ Get all data from database for all meetings. """
    
    all_meetings = crud.get_all_meetings()
    meeting_dict = [meeting.to_dict() for meeting in all_meetings]
    return jsonify(meeting_dict)



if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='localhost') # localhost preferable for video api
    