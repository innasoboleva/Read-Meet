import json, os, time, jsonify
import requests
import urllib.parse # for URL encoding
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By # for searching tags by condition
from selenium.webdriver.support.wait import WebDriverWait # for waiting to load the Selenium request
from selenium.webdriver.support import expected_conditions as EC    # adding condition
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException     # exception when loading

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
book_page = "https://www.goodreads.com/search?q=" # find search and insert ISBN
book_reviews = "https://www.goodreads.com/book/show/{}/reviews?"

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
        

# isbn considered as a string here
def find_page_selenium(isbn):
    """
    Gets Goodreads page and makes search for the book by it's isbn. If book exists, returns dict with 'url': url that has local Goodreads ID.
    If book doesn't exist, returns dict with status: error.
    """
    driver = webdriver.Chrome()
    # searching for book by it's isbn, passing query parameter in url
    base_url = book_page + isbn
    driver.get(base_url)
    try:
        header = driver.find_element(By.TAG_NAME, 'h1')
        if header.get_property('innerText') == 'Search':
            return jsonify({ 'status': 'error', 'code': 204, 'message': 'Book was not found on Goodreads', 'url': None })
    except:
        pass
    try:
        WebDriverWait(driver, 30).until(EC.url_changes(base_url))
        # redirected url, for the ID on Goodreads for exact book 
        new_url = driver.current_url
        driver.quit()
        return jsonify({ 'status': 'success', 'code': 200, 'message': 'OK', 'url': new_url })
    except:
        return jsonify({ 'status': 'error', 'code': 404, 'message': 'Page for getting Goodreads ID was not loaded.', 'url': None })


def find_book_number_selenium(url_data):
    """
    Strips url from dict url_data, if exists, to get Goodreads local ID for the required book. If no url, returns the url_data.
    """
    if url_data['status'] == 'success':
        last_part = url_data['url'].split('/')[-1]
        goodreads_number = last_part.split('-')[0]
        return jsonify({ 'status': 'success', 'code': 200, 'message': 'OK', 'goodreads_book_id': goodreads_number })
    return url_data

def find_reviews_selenium(data, occurance):
    """ 
    Provides review information for given book number in Goodreads app, if book present on Goodreads. If not, returns data.
    """
    goodreads_book_id = data.get('goodreads_book_id', None)
    if goodreads_book_id:
        driver = webdriver.Chrome()
        driver.get(book_reviews.format(goodreads_book_id))
        try:
            # waiting for rating stars to load as indicator that all needed info has been loaded
            WebDriverWait(driver, 200).until(lambda x: x.find_elements(By.CLASS_NAME, 'RatingStars'))
            review_cards = WebDriverWait(driver, 130).until(lambda x: x.find_elements(By.CLASS_NAME, 'ReviewCard'))
            reviews_for_book = []
            for card in review_cards:
                review = {}
                # gets user's name
                name = card.find_element(By.XPATH, './/div[@class="ReviewerProfile__name"]')
                review['name'] = name.get_property("textContent")
                # text of the review
                text = card.find_element(By.XPATH, './/span[@class="Formatted"]')
                review['text'] = text
                # timestamp
                day = card.find_elements(By.XPATH, './/span[contains(@class, "Text__body3")]')
                if len(day) == 2:
                    review['day'] = day[1].get_property("textContent")
                elif len(day) == 3:
                    review['day'] = day[2].get_property("textContent")
                else:
                    review['day'] = 'No date available'
                # given stars
                try:
                    stars = card.find_element(By.XPATH, './/span[contains(@class, "RatingStars")]')
                    review['stars'] = stars.get_attribute('aria-label')
                except:
                    review['stars'] = ''
                    continue
                reviews_for_book.append(review)
            
            return jsonify({ 'status': 'success', 'code': 200, 'message': 'OK', 'reviews': reviews_for_book })

        except TimeoutException:
            return jsonify({ 'status': 'error', 'code': 404, 'message': 'Page for reading elements for reviews did not load.', 'url': None })
        except:
            return jsonify({ 'status': 'error', 'code': 404, 'message': 'Target element for reviews did not render.', 'url': None })
        finally:
            if driver:
                driver.quit()
    else:
        return data


# Get information from reviews
def get_review_info():
    pass

# Get thirty reviews
def get_reviews_count(count):
    pass


print(find_book_number_selenium(find_page_selenium('9780735276482')))