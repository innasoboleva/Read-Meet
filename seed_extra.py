# File for seeding the database
from datetime import datetime, timedelta
import random
import string
import pytz

import models, server
import csv
import sys

csv.field_size_limit(sys.maxsize)
csv_file_path = 'parks.csv'


models.connect_to_db(server.app)
models.db.create_all()

addresses_found = []

with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    column_index = 2  
    for row in reader:
        if len(row) > column_index:
            address = row[column_index].strip()  # Assuming the address is in the specified column.
            if address is not None and address != "":
                addresses_found.append(address)


# generates random string
def generate_random_string(length):
    characters = string.ascii_lowercase  # Use any character set you prefer
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

# creating lists for users
users = models.User.query.all()

# creates meetings
books = models.Book.query.all()
for index, user in enumerate(users):
    date_now = datetime.now() + timedelta(days=random.randint(1, 20)) # adding one more day to now
    nyc = pytz.timezone('America/New_York')
    date_localized = nyc.localize(date_now)
    offline = random.choice([False,True])
    place = random.choice(addresses_found)
    random_book = books[random.randint(0, len(books) - 1)]
    random_guests_num = random.randint(3, 15)
    new_meeting = models.Meeting.create(random_book, date_localized, offline, user, random_guests_num, place=place) # book, day, offline, host, max_guests, video_note=None, overview=None, place=None, address=None, language="EN"
    
    models.db.session.add(new_meeting)
    random_guests = random.randint(0, random_guests_num)
    for _ in range(random_guests):
        num = random.randint(0, len(users)-1)
        while num == index:
            num = random.randint(0, len(users)-1)
        new_meeting.attending_guests.append(users[num])

models.db.session.commit()