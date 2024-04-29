from models import db, connect_to_db
import crud
from server import app

with app.app_context():
    connect_to_db(app)
    db.create_all()
    # every month in prod
    crud.add_new_popular_books_to_db()

# updating old meetings to inactive
crud.update_past_meetings()
# save changes
db.session.commit()

# every month books needs to be uploaded
crud.delete_old_unused_books_from_db()