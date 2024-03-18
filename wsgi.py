from server import app
from models import connect_to_db, db

if __name__ == '__main__':
    app.run(debug=False)

