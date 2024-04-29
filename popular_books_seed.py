from models import db, connect_to_db
import crud
from server import app

with app.app_context():
    # every month in prod
    crud.add_new_popular_books_to_db()
    # updating old meetings to inactive
    crud.update_past_meetings()
    # every month books needs to be uploaded
    crud.delete_old_unused_books_from_db()
    # save changes
    db.session.commit()