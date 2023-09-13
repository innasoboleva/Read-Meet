# File for seeding the database
import os
import json
from datetime import datetime, timedelta
import random
import string
import pytz

import models, server
from apis import books_api, goodreads_api


os.system('dropdb readmeet')
os.system('createdb readmeet')

models.connect_to_db(server.app)
models.db.create_all()

# generates random string
def generate_random_string(length):
    characters = string.ascii_lowercase  # Use any character set you prefer
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

# filling User table with JSON data
users_data = []
with open('users.json', 'r') as file:
    users_data = json.load(file)

for user in users_data:
    new_user = models.User.create(user['email'], user['password'], user['name'], int(user['zipcode']), user['address'], int(user['age']))
    models.db.session.add(new_user)

models.db.session.commit()

# getting popular books, filling book table for now
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
                book_id = popular_book.get("book_id")
                title = popular_book.get("title")
                subtitle = popular_book.get("subtitle")
                authors = popular_book.get("authors")
                description = popular_book.get("description")
                books_ISBN = popular_book.get("ISBN")
                image = popular_book.get("image_url")
                popular_book = datetime.today().strftime("%Y-%m")
                new_book = models.Book.create(book_id=book_id, isbn=books_ISBN, title=title, subtitle=subtitle, authors=authors, \
                  image_url=image, description=description, popular_book=popular_book)
                models.db.session.add(new_book)

models.db.session.commit()

# creating lists for users
users = models.User.query.all()
for user in users:
    name = generate_random_string(6)
    number = random.randint(0, 100)
    list_name = name + str(number)
    new_list = models.List.create(list_name, user)
    models.db.session.add(new_list)

# creates meetings
books = models.Book.query.all()
for index, user in enumerate(users):
    date_now = datetime.now() + timedelta(days=1) # adding one more day to now
    nyc = pytz.timezone('America/New_York')
    date_localized = nyc.localize(date_now)

    random_book = books[random.randint(0, len(books) - 1)]
    random_guests_num = random.randint(5, 25)
    new_meeting = models.Meeting.create(random_book, date_localized, True, user, random_guests_num) # book, day, offline, host, max_guests, video_note=None, overview=None, place=None, address=None, language="EN"
    models.db.session.add(new_meeting)
    random_guests = random.randint(0, random_guests_num)
    for _ in range(random_guests):
        num = random.randint(0, len(users)-1)
        while num == index:
            num = random.randint(0, len(users)-1)
        new_meeting.attending_guests.append(users[num])

models.db.session.commit()