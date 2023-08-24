# File for seeding the database
import os
import json

import models
import crud
import server
from apis import books_api, yelp_api, goodreads_api
from datetime import datetime

os.system('dropdb readmeet')
os.system('createdb readmeet')

models.connect_to_db(server.app)
models.db.create_all()


users_data = []
with open('users.json', 'r') as file:
    users_data = json.load(file)

for user in users_data:
    new_user = models.User.create(user['email'], user['password'], user['name'], int(user['zipcode']), user['address'], int(user['age']))
    models.db.session.add(new_user)

models.db.session.commit()

popular_books = goodreads_api.get_books_for_carousel()
status = popular_books.get("status")
if status == "success":
    list_of_titles = popular_books.get("titles")
    for book in list_of_titles:
        result_from_book_search = books_api.find_popular_book(book)
        book_status = result_from_book_search.get("status")
        if book_status == "success":
            books = result_from_book_search.get("books")
            if books:
                popular_book = books[0]
                title = books[0].get("title")
                subtitle = books[0].get("subtitle")
                authors = books[0].get("authors")
                description = books[0].get("description")
                books_ISBN = books[0].get("ISBN")
                image = books[0].get("image")
                popular_book = datetime.now().date()
                new_book = models.Book.create(isbn=books_ISBN, title=title, subtitle=subtitle, authors=authors, \
                  image_url=image, description=description, popular_book=popular_book)
                models.db.session.add(new_book)

models.db.session.commit()

