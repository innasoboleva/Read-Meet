# Adding comments
from selenium import webdriver
from selenium.webdriver.common.by import By # for searching tags by condition
from selenium.webdriver.support.wait import WebDriverWait # for waiting to load the Selenium request
from selenium.webdriver.support import expected_conditions as EC    # adding condition
from selenium.common.exceptions import TimeoutException  # exception when loading
from datetime import datetime

# getting Goodreads reviews and choice of books
new_books = "https://www.goodreads.com/book/popular_by_date/{}/{}" # insert a year like 2023 and month as 1 - Jan, 2 - Feb
book_page = "https://www.goodreads.com/search?q=" # insert book's ISBN
book_reviews = "https://www.goodreads.com/book/show/{}/reviews?" # Goodreads book ID goes here


# isbn considered as a string here
def _find_page_selenium(isbn):
    """
    Gets Goodreads page and makes search for the book by it's isbn. If book exists, method returns dict with key 'url' that has local Goodreads ID.
    If book doesn't exist, method returns dict with status = error.
    """
    driver = webdriver.Chrome()
    # searching for book by it's isbn, passing query parameter in url
    base_url = book_page + isbn
    driver.get(base_url)
    try:
        header = WebDriverWait(driver, 20).until(lambda x: x.find_element(By.TAG_NAME, 'h1'))
        if header.text == 'Search':
            print("BOOK IS NOT ON GOODREADS")
            return { "status": "error", "code": 204, "message": "Book was not found on Goodreads", "url": None }
        elif header.text == '404':
            return { "status": "error", "code": 404, "message": "Goodreads does not respond" }
        else:
            # redirected url, for the ID on Goodreads for exact book 
            new_url = driver.current_url
            return { "status": "success", "code": 200, "message": "OK", "url": new_url }
    except:
        return { "status": "error", "code": 404, "message": "Page for getting Goodreads ID was not loaded.", "url": None }
    finally:
            driver.quit()


def _find_book_number_selenium(url_data):
    """
    Strips url from dict url_data, if exists, to get Goodreads local ID for the required book. If no url, returns the url_data.
    """
    if url_data['status'] == 'success':
        last_part = url_data['url'].split('/')[-1]
        goodreads_number = last_part.split('-')[0]
        return { "status": "success", "code": 200, "message": "OK", "goodreads_book_id": goodreads_number }
    return url_data


def _find_reviews_selenium(data, occurance=1):
    """ 
    Provides review information for given book number in Goodreads app, if book present on Goodreads. If not, returns data back.
    """
    goodreads_book_id = data.get('goodreads_book_id', None)
    if goodreads_book_id:
        driver = webdriver.Chrome()
        
        driver.get(book_reviews.format(goodreads_book_id))
        try:
            header = WebDriverWait(driver, 30).until(lambda x: x.find_element(By.TAG_NAME, 'h1'))
            if header.text == '404':
                print("BOOK IS NOT ON GOODREADS")
                return { "status": "error", "code": 204, "message": "Book was not found on Goodreads", \
                        "url": None, "message": "No reviews are available for this book." }
            # waiting for rating stars to load as indicator that all needed info has been loaded
            error = driver.find_elements(By.CLASS_NAME, 'ErrorCard') 
            if error:
                print("Book has no reviews.")
                return { "status": "error", "code": 204, "message": "Book was not found on Goodreads", \
                        "url": None, "message": "No one has reviewed this book yet." }
            review_cards = WebDriverWait(driver, 30).until(lambda x: x.find_elements(By.CLASS_NAME, 'ReviewCard'))
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
            return { "status": "success", "code": 200, "message": "OK", "reviews": reviews_for_book }

        except TimeoutException:
            return { "status": "error", "code": 404, "message": "Page for reading elements for reviews did not load.", "url": None }
        except Exception as error:
            return { "status": "error", "code": 404, "message": f"Target element for reviews did not render. {str(error)}", "url": None }
        finally:
            driver.quit()
    else:
        return data
    

def get_reviews(isbn):
    """
    Public method for getting reviews for a book.
    """
    result_from_url = None
    count_url = 0 # trying to get page url 2 times
    while count_url <= 2:
        count_url += 1
        result_from_url = _find_page_selenium(isbn)
        if result_from_url.get("status") == "error" and result_from_url.get("code") != 204:
            print("Trying to get url for getting reviews one more time...")
            continue
        elif result_from_url.get("code") == 204:
            return result_from_url
        else:
            break
    
    id = _find_book_number_selenium(result_from_url)

    reviews = None
    count_reviews = 0   # trying to get reviews 2 times

    while id.get("status") == "success" and count_reviews <= 3:
        count_reviews += 1
        reviews = _find_reviews_selenium(id)
        if reviews.get("status") == "error" and reviews.get("code") != 204:
            print("Trying to get reviews one more time...")
            continue
        elif reviews.get("code") == 204:
            return reviews
        else:
            break
    return reviews


def _get_popular_books(current_date):
    """ 
    Returns list of tuples with about 15 popular books for the requested month.
    Current date is a tuple, containing year (first) and month (second).
    
    """
    base_url = new_books.format(current_date[0], current_date[1])
    driver = webdriver.Chrome()
    # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(base_url)
    titles = []
    authors = []
    try:
        books_titles = WebDriverWait(driver, 60).until(lambda x: x.find_elements(By.CLASS_NAME, 'Text__title3'))
        books_authors = WebDriverWait(driver, 60).until(lambda x: x.find_elements(By.CLASS_NAME, 'Text__h3'))
        longest = min(len(books_titles), len(books_authors))
        for i in range(longest): # iterating as many times as we got book title or authors
            title = books_titles[i].text
            titles.append(title)
            author = books_authors[i].text
            authors.append(author)
        return { "status": "success", "code": 200, "message": "OK", "titles": list(zip(titles, authors)) }
    except TimeoutException:
        return { "status": "error", "code": 404, "message": "Page for popular books did not load.", "url": None }
    except:
        return { "status": "error", "code": 404, "message": "Unexpected error loading elements (popular books). Not found." }
    finally:
        driver.quit()


def _get_current_date():
    """ Returns tuple with current year and current month. """

    today = datetime.now()
    year = today.year
    month = today.month - 1
    if month == 0:  # fix for January
        month = 12
        year -= 1
    return (year, month)


def get_books_for_carousel():
    """
    Public method for getting json with a list of tuples with about 15 popular books for the current month.
    """
    today = _get_current_date()
    result = _get_popular_books(today)
    return result


