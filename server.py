# import os
# from apis import books_api, yelp_api, goodreads_api
from flask import Flask, render_template
# from models import connect_to_db , db, User
from models import connect_to_db
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev" # os.environ.get('FLASK_KEY')
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("base.html")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0') # localhost preferable for video api
    