from models import db
import crud

# updating old meetings to inactive
crud.update_past_meetings()
# save changes
db.session.commit()

# every month books needs to be uploaded
crud.delete_old_unused_books_from_db()
crud.add_new_popular_books_to_db()