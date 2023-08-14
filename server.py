from apis import books_api, yelp_api, goodreads_api
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("base.html")


if __name__ == "__main__":
    app.run(debug=True, host='localhost')