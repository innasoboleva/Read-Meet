from selenium import webdriver
from selenium.webdriver.common.by import By # for searching tags by condition
from selenium.webdriver.support.wait import WebDriverWait # for waiting to load the Selenium request
from selenium.webdriver.support import expected_conditions as EC    # adding condition
from selenium.common.exceptions import TimeoutException  # exception when loading

# getting Goodreads reviews and choice of books
best_books = "https://www.goodreads.com/choiceawards/best-books-2022"
book_page = "https://www.goodreads.com/search?q=" # insert book's ISBN
book_reviews = "https://www.goodreads.com/book/show/{}/reviews?" # Goodreads book ID goes here


# isbn considered as a string here
def find_page_selenium(isbn):
    """
    Gets Goodreads page and makes search for the book by it's isbn. If book exists, method returns dict with key 'url' that has local Goodreads ID.
    If book doesn't exist, method returns dict with status = error.
    """
    driver = webdriver.Chrome()
    # searching for book by it's isbn, passing query parameter in url
    base_url = book_page + isbn
    driver.get(base_url)
    try:
        header = driver.find_element(By.TAG_NAME, 'h1')
        if header.get_property('innerText') == 'Search':
            return { 'status': 'error', 'code': 204, 'message': 'Book was not found on Goodreads', 'url': None }
    except:
        pass
    try:
        WebDriverWait(driver, 30).until(EC.url_changes(base_url))
        # redirected url, for the ID on Goodreads for exact book 
        new_url = driver.current_url
        driver.quit()
        return { 'status': 'success', 'code': 200, 'message': 'OK', 'url': new_url }
    except:
        return { 'status': 'error', 'code': 404, 'message': 'Page for getting Goodreads ID was not loaded.', 'url': None }


def find_book_number_selenium(url_data):
    """
    Strips url from dict url_data, if exists, to get Goodreads local ID for the required book. If no url, returns the url_data.
    """
    if url_data['status'] == 'success':
        last_part = url_data['url'].split('/')[-1]
        goodreads_number = last_part.split('-')[0]
        return { 'status': 'success', 'code': 200, 'message': 'OK', 'goodreads_book_id': goodreads_number }
    return url_data

def find_reviews_selenium(data, occurance=1):
    """ 
    Provides review information for given book number in Goodreads app, if book present on Goodreads. If not, returns data back.
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
                # text of the review, including inner formatting
                text = card.find_element(By.XPATH, './/span[@class="Formatted"]')
                overview = text.get_property("innerHTML")
                review['text'] = overview
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
            
            return { 'status': 'success', 'code': 200, 'message': 'OK', 'reviews': reviews_for_book }

        except TimeoutException:
            return { 'status': 'error', 'code': 404, 'message': 'Page for reading elements for reviews did not load.', 'url': None }
        except:
            return { 'status': 'error', 'code': 404, 'message': 'Target element for reviews did not render.', 'url': None }
        finally:
            if driver:
                driver.quit()
    else:
        return data
    

def get_reviews(isbn):
    """
    Getting reviews for a book.
    """
    url = find_page_selenium(isbn)
    id = find_book_number_selenium(url)
    reviews = find_reviews_selenium(id)
    return reviews

# print(get_reviews('9780735276482'))