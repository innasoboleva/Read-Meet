import requests, os
from urllib.parse import quote # for encoding search queries

# set up for books API requests
book_key = os.environ.get('BOOK_KEY')
book_url = "https://www.googleapis.com/books/v1/volumes?q=" # add search args to the url
book_isbn = "https://www.googleapis.com/books/v1/volumes?q=isbn:" # find form action=/search and add ISBN number


# def find_books(params):
#     """
#     Using Google books API, looks for a list of books, adding parameters to a search query. Returns 20 books. 
#     """
#     book_search_url = book_url + params
#     headers = {
#             'Content-type': 'application/json',
#             'Authorization': book_key
#         }
#     response = requests.get(book_search_url, headers=headers)
#     if response.status_code == 200:
#         response_data = response.json()
#         books = response_data.get('items', [])
#         count = 0
#         # variables to help splitting results / pagination
#         page_start = 0
#         page_end = 20
#         books_to_render = []
#         for book in books[page_start:page_end]:
#             volume_info = book.get('volumeInfo', None)
#             if volume_info:
#                 book_to_add = {}
#                 title = volume_info.get('title', '') # check if this is in a data from Books API
#                 book_to_add['title'] = title
#                 subtitle = volume_info.get('subtitle', '')
#                 book_to_add['subtitle'] = subtitle
#                 authors = volume_info.get('authors', ['No authors available.'])
#                 authors_str = ', '. join(authors)
#                 book_to_add['authors'] = authors_str
#                 description = volume_info.get('description', 'No description available.')
#                 book_to_add['description'] = description
#                 industry_identifiers = volume_info.get('industryIdentifiers', [])
#                 ISBN_13 = None
#                 ISBN_10 = None
#                 if len(industry_identifiers) > 1:
#                     ISBN = [item for item in industry_identifiers if item.get('type') == 'ISBN_13']
#                     if ISBN:
#                         ISBN_13 = ISBN[0].get('identifier', None)
#                 if not ISBN_13:
#                     ISBN = [item for item in industry_identifiers if item.get('type') == 'ISBN_10']
#                     if ISBN:
#                         ISBN_10 = ISBN[0].get('identifier', None)
#                         book_to_add['ISBN'] = ISBN_10
#                 book_to_add['ISBN'] = ISBN_13
#                 image_links = volume_info.get('imageLinks', None)
#                 if image_links:
#                     image_link = image_links.get('thumbnail', '/static/img/basic_thumbnail.png') # if picture is not present, there is standart thumbnail
#                     book_to_add['image'] = image_link
#                 else:
#                     book_to_add['image'] = '/static/img/basic_thumbnail.png'
#                 books_to_render.append(book_to_add)
#             count += 1
#             if count == 5:
#                 break
            
#         if books_to_render:
#             return { 'status': 'success', 'code': 200, 'message': 'OK', 'books': books_to_render }
#         else:
#             return { 'status': 'error', 'code': 204, 'message': 'Google books could not find any results' }
#     else:
#          return { 'status': 'error', 'code': 404, 'message': 'Could not get Google books data, server does not respond.' }


def _get_search_result_for_params(param, on_page=20):
    """
    Using Google books API, get a response from Google books, with provided parameters. Returns JSON response.
    """
    book_search_url = book_url + param
    headers = {
            'Content-type': 'application/json',
            'Authorization': book_key
        }
    response = requests.get(book_search_url, headers=headers)
    if response.status_code == 200:
        return { "status": "success", "response": response.json(), "on_page": on_page }
    else:
        return { "status": "error", "code": 404, "message": "Could not get Google books data, server does not respond." }


def _get_list_of_books_for_page(search_result, count=0):
    """
    With provided response, returns book information. Count = how many pages to skip.
    """
    response = search_result.get("status")
    if response == "success":
        try:
            response_data = search_result.get("response")
            books = response_data.get('items', [])
            on_page = search_result.get("on_page", 20)
            start = count * on_page
            end = count * on_page + on_page # to help splitting results / pagination -- every 20 results
            return _get_books_info_from_response(books, start, end)
        except:
            return { 'status': 'error', 'code': 404, 'message': 'Exception. No data in response. Could not get Google books data.' }
    else:
        return search_result


def _get_books_info_from_response(items, start, stop):
    """
    Returns desired ammount of books from response. Or json respose with status 'error'.
    Items - list from response from search query. Start - starting point of iteration, stop - it's end.
    """
    books_to_render = []
    for book in items[start:stop]:
        volume_info = book.get('volumeInfo', None)
        if volume_info:
            book_to_add = {}
            title = volume_info.get('title', '') # check if this is in a data from Books API
            book_to_add['title'] = title
            subtitle = volume_info.get('subtitle', '')
            book_to_add['subtitle'] = subtitle
            authors = volume_info.get('authors', ['No authors available.'])
            authors_str = ', '. join(authors)
            book_to_add['authors'] = authors_str
            description = volume_info.get('description', 'No description available.')
            book_to_add['description'] = description
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
                    book_to_add['ISBN'] = ISBN_10
            book_to_add['ISBN'] = ISBN_13
            image_links = volume_info.get('imageLinks', None)
            if image_links:
                image_link = image_links.get('thumbnail', '/static/img/basic_thumbnail.png') # if picture is not present, there is standart thumbnail
                book_to_add['image'] = image_link
            else:
                book_to_add['image'] = '/static/img/basic_thumbnail.png'
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


def find_list_of_books(params):
    """
    Using Google books API, looks for a list of books, adding parameters to a search query. Returns 20 books. 
    """
    parameters = quote(params)
    response = _get_search_result_for_params(parameters)  # will show only first 20 books
    result = _get_list_of_books_for_page(response)
    return result
