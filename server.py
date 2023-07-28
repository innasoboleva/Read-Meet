import json, os
import requests
import urllib.parse # for URL encoding
from bs4 import BeautifulSoup
from models import *

# set up for books API requests
book_key = os.environ.get('BOOK_KEY')
book_url = "https://www.googleapis.com/books/v1/volumes?q=" # add search args to the url
book_isbn = "https://www.googleapis.com/books/v1/volumes?q=isbn:" # find form action=/search and add ISBN number

# set up for yelp API requests
yelp_key = os.environ.get('YELP_KEY')
yelp_id = os.environ.get('YELP_ID')
yelp_url = "https://api.yelp.com/v3/businesses/search?location={}&term={}" # term is keyword as park or cafe, location can be address or zipcode

# getting Goodreads reviews and choice of books
best_books = "https://www.goodreads.com/choiceawards/best-books-2022"
book_reviews = "https://www.goodreads.com" # find search and insert ISBN

# collection of our users (not real)
users = []

def get_users():
    users_data = []
    with open('users.json', 'r') as file:
        users_data = json.load(file)
    for user in users_data:
        User(user['name'], user['email'], user['password'], user['zipcode'], user['address'], user['age'])


def find_book(params):
    book_search_url = book_url + params
    headers = {
            'Content-type': 'application/json',
            'Authorization': book_key
        }
    response = requests.get(book_search_url, headers=headers).json()
    if response.status_code == 200:
        books = response.get('items', [])
        count = 0
        for book in books[:20]:
            volume_info = book.get('volumeInfo', None)
            if volume_info:
                title = volume_info.get('title', '') # check if this is in a data from Books API
                subtitle = volume_info.get('subtitle', '')
                authors = volume_info.get('authors', ['No authors available.'])
                authors_str = ', '. join(authors)
                description = volume_info.get('description', 'No description available.')
                image_links = volume_info.get('imageLinks', None)
                industry_identifiers = volume_info.get('industryIdentifiers', [])
                ISBN_13 = None
                ISBN_10 = None
                if len(industry_identifiers) > 1:
                    ISBN = [item for item in industry_identifiers if item.get('type') == 'ISBN_13']
                    if ISBN:
                        ISBN_13 = ISBN[0].get('identifier', None)
                if not ISBN_13:
                    ISBN = [item for item in industry_identifiers if item.get('type') == 'ISBN_10']
                    if ISBN:
                        ISBN_10 = ISBN[0].get('identifier', None)
                if image_links:
                    image_link = image_links.get('thumbnail', '/static/img/basic_thumbnail.png') # if picture is not present, there is standart thumbnail
            count += 1
            if count == 5:
                break


def find_places(zipcode, type):
    yelp_search_url = yelp_url.format(zipcode, type)
    yelp_search_url_encoded = urllib.parse.quote(yelp_search_url)
    headers = {
            'Content-type': 'application/json',
            'Authorization': f'Bearer {yelp_key}'
        }
    response = requests.get(yelp_search_url, headers=headers).json()
    if response.status_code == 200:
        places = response.get('businesses', [])
        for place in places[:20]:
            url = place.get('url', '')
            name = place.get('name', '')
            image_url = place.get('image_url', '')
            location = place.get('location', '')
            if location:
                address = location.get('display_address', '')
        
    
def find_reviews(isbn):

    response = requests.get(book_reviews)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        search_form = soup.find_all('a')

# get_users()
# find_book('peanut')