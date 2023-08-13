import requests, os

# set up for books API requests
book_key = os.environ.get('BOOK_KEY')
book_url = "https://www.googleapis.com/books/v1/volumes?q=" # add search args to the url
book_isbn = "https://www.googleapis.com/books/v1/volumes?q=isbn:" # find form action=/search and add ISBN number


def find_book(params):
    """
    Using Google books API, looks for a list of books, adding parameters to a search query.
    """
    book_search_url = book_url + params
    headers = {
            'Content-type': 'application/json',
            'Authorization': book_key
        }
    response = requests.get(book_search_url, headers=headers).json()
    if response.status_code == 200:
        books = response.get('items', [])
        count = 0
        # variables to help splitting results / spagination
        page_start = 0
        page_end = 20
        books_to_render = []
        for book in books[page_start:page_end]:
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
            count += 1
            if count == 5:
                break
        if books_to_render:
            return { 'status': 'success', 'code': 200, 'message': 'OK', 'books': books_to_render }
        else:
            return { 'status': 'error', 'code': 204, 'message': 'Google books could not find any results' }
    else:
         return { 'status': 'error', 'code': 404, 'message': 'Could not get Google books data, server does not respond.' }
