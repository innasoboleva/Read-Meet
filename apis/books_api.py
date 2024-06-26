import requests, os, json
from urllib.parse import quote # for encoding search queries
import random

# set up for books API requests
book_key = os.environ.get('BOOK_KEY')
book_url = "https://www.googleapis.com/books/v1/volumes?q=" # add search args to the url
book_url_with_id = "https://www.googleapis.com/books/v1/volumes/" # id + ?key=yourKey


def _get_random_search_param():
    """ 
    Returns random word from the call to free data. 
    Using this list: https://github.com/bevacqua/correcthorse/blob/master/wordlist.json
    """

    words = []
    with open('wordlist.json', 'r') as f:
        words = json.load(f)
    word = random.choice(words)
    print("WORD: ", word)
    return quote(word)


def _get_search_result_for_params(param, page=0, on_page=None):
    """
    Using Google books API, get a response from Google books, with provided parameters. Need to specify page. Each has 40 results. Returns JSON response.
    """
    search_param = param
    if param is None:
        search_param = _get_random_search_param()
    page_results = 40
    max_results = "&maxResults=40"
    s_page = page * page_results
    star_index = f"&startIndex={s_page}"
    book_key_param = f'&key={book_key}'
    book_search_url = book_url + search_param + max_results + star_index + book_key_param
    response = requests.get(book_search_url)
    print(book_search_url)
    print(response)
    if (response.status_code == 200):
        return { "status": "success", "response": response.json(), "on_page": on_page }
    else:
        return { "status": "error", "code": 404, "message": "Could not get Google books data, server does not respond." }


def _get_list_of_books_for_page(search_result):
    """
    With provided response, returns book information. Count = how many pages to skip.
    """
    if search_result.get("status") == "success":
        try:
            response_data = search_result.get("response")
            books = response_data.get('items', [])
            on_page = search_result.get("on_page", None)
            if on_page: # to help splitting results / pagination or to display 1 book only
                return _get_books_info_from_response(books, start=0, stop=on_page)
            else:
                return _get_books_info_from_response(books) # get all results
        except:
            return { 'status': 'error', 'code': 404, 'message': 'Exception. No data in response. Could not get Google books data.' }
    else:
        return search_result


def _get_books_info_from_response(items, start=None, stop=None):
    """
    Returns desired ammount of books from response. Or json respose with status 'error'.
    Items - list from response from search query. Start - starting point of iteration, stop - it's end.
    """
    books_to_render = []

    if stop:
        items_list = items[start:stop]
    else:
        items_list = items
    for book in items_list:
        book_id = book.get('id', None)
        volume_info = book.get('volumeInfo', None)
        if volume_info and book_id:
            book_to_add = { "book_id": book_id }
            title = volume_info.get('title', '') # check if this is in a data from Books API
            book_to_add['title'] = title
            subtitle = volume_info.get('subtitle', '')
            book_to_add['subtitle'] = subtitle
            authors = volume_info.get('authors', ['No authors available'])
            authors_str = ', '. join(authors)
            book_to_add['authors'] = authors_str
            description = volume_info.get('description', 'No description available.')
            book_to_add['description'] = description
            industry_identifiers = volume_info.get('industryIdentifiers', [])
            if industry_identifiers == []:
                book_to_add['ISBN'] = None
            else:
                ISBN_13 = None
                ISBN_10 = None
                ISBN_13 = [item for item in industry_identifiers if item.get('type') == 'ISBN_13']
                ISBN_10 = [item for item in industry_identifiers if item.get('type') == 'ISBN_10']
                if ISBN_13:
                    book_to_add['ISBN'] = ISBN_13[0]["identifier"]
                elif ISBN_10:
                    book_to_add['ISBN'] = ISBN_10[0]["identifier"]
                else: # can be something like 'type': 'OTHER', 'identifier': 'UOM:39015000639784'}
                    book_to_add['ISBN'] = industry_identifiers[0]["identifier"]
            image_links = volume_info.get('imageLinks', None)
            if image_links:
                image_link = image_links.get('thumbnail', '/static/img/basic_thumbnail.png') # if picture is not present, there is standart thumbnail
                book_to_add['image_url'] = image_link
            else:
                book_to_add['image_url'] = '/static/img/basic_thumbnail.png'
            books_to_render.append(book_to_add)
    if books_to_render:
        return { 'status': 'success', 'code': 200, 'message': 'OK', 'books': books_to_render }
    else:
        return { 'status': 'error', 'code': 204, 'message': 'Google books could not find any results' }
    

def find_popular_book(info):
    """
    Returns first book in a list from google books with parameters as title and author provided in tuple 'info'.
    """
    if info:
        parameters = quote(f"intitle:{info[0]}+inauthor:{info[1]}")
        response = _get_search_result_for_params(parameters, on_page=1) # only need 1 first book
        result = _get_list_of_books_for_page(response)
        return result
    else:
        return { 'status': 'error', 'code': 404, 'message': 'No tuple with book information was provided for the search.' }


def find_list_of_books(params, page):
    """
    Using Google books API, looks for a list of books, adding parameters to a search query. Returns 20 books. 
    """
    parameters = None
    if params:
        parameters = quote(params) # to fix all spaces
    response = _get_search_result_for_params(parameters, page)
    result = _get_list_of_books_for_page(response)
    return result


def _get_response_for_book_ID(book):
    """ Getting response from server for book with provided book ID """
    key = f"?key={book_key}"
    book_search_url = book_url_with_id + book + key
    print("Book search URL:", book_search_url)
    response = requests.get(book_search_url)
    
    if (response.status_code == 200):
        return { "status": "success", "response": response.json() }
    else:
        return { "status": "error", "code": 404, "message": f"Could not get book with ID: s{book}, server does not respond." }


def _get_book_for_book_ID(response):
    """ Getting information from response and passing it in a dictionary """

    if response.get("status") == "success":
        new_book = {}
        item = response.get("response")
        book_id = item.get("id")
        new_book["book_id"] = book_id

        volume_info = item.get('volumeInfo')
        title = volume_info.get('title', '') # check if this is in a data from Books API
        new_book['title'] = title
        subtitle = volume_info.get('subtitle', '')
        new_book['subtitle'] = subtitle
        authors = volume_info.get('authors', ['No authors available'])
        authors_str = ', '. join(authors)
        new_book['authors'] = authors_str
        description = volume_info.get('description', 'No description available.')
        new_book['description'] = description
        industry_identifiers = volume_info.get('industryIdentifiers', [])
        if industry_identifiers == []:
            new_book["ISBN"] = None
        else:
            ISBN_13 = None
            ISBN_10 = None
            ISBN_13 = [item for item in industry_identifiers if item.get('type') == 'ISBN_13']
            ISBN_10 = [item for item in industry_identifiers if item.get('type') == 'ISBN_10']
            if ISBN_13:
                new_book['ISBN'] = ISBN_13[0]["identifier"]
            elif ISBN_10:
                new_book['ISBN'] = ISBN_10[0]["identifier"]
            else: # can be something like 'type': 'OTHER', 'identifier': 'UOM:39015000639784'}
                new_book['ISBN'] = industry_identifiers[0]["identifier"]
        
        image_links = volume_info.get('imageLinks', None)
        if image_links:
            image_link = image_links.get('thumbnail', '/static/img/basic_thumbnail.png') # if picture is not present, there is standart thumbnail
            new_book['image_url'] = image_link
        else:
            new_book['image_url'] = '/static/img/basic_thumbnail.png'

        return { "status": "success", "book": new_book }
    else:
        return { "status": "error", "code": 404, "message": f"Could not get book with ID: s{book_id}, server does not respond." }


def find_book(book_id):
    """
    Return result of search for certain ID.
    """
    response = _get_response_for_book_ID(book_id)
    return _get_book_for_book_ID(response)

