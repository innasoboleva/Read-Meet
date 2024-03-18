from server import app
from models import connect_to_db, db

if __name__ == '__main__':
    app.run(debug=False)

    with app.app_context():
        connect_to_db(app)
        db.create_all()