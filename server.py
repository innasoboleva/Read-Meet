import os
from apis import books_api, yelp_api, goodreads_api
from flask import Flask, render_template
from models import connect_to_db, db, User

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_KEY')


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("base.html")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='localhost') # localhost preferable for video api
    