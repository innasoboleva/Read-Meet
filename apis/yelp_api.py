import requests, os
import urllib.parse # for URL encoding


# set up for yelp API requests
yelp_key = os.environ.get('YELP_KEY')
yelp_url = "https://api.yelp.com/v3/businesses/search?location={}&term={}" # term is keyword as park or cafe, location can be address or zipcode

def find_places(zipcode, type):
    """
    Using Yelp API, method gets information for local businesses and returns a list of dictionaries with the result.
    Need zipcode and type of business to search for, park or cafe for example.
    """
    yelp_search_url = yelp_url.format(zipcode, type)
    yelp_search_url_encoded = urllib.parse.quote(yelp_search_url)
    headers = {
            'Content-type': 'application/json',
            'Authorization': f'Bearer {yelp_key}'
        }
    response = requests.get(yelp_search_url_encoded, headers=headers).json()
    if response.status_code == 200:
        places_to_display = []
        places = response.get('businesses', [])
        # for pagination puposes
        page_start = 0
        page_end = 20
        for place in places[page_start:page_end]:
            place = {}
            url = place.get('url', '')
            place['url'] = url
            name = place.get('name', '')
            place['name'] = name
            image_url = place.get('image_url', '')
            place['image'] = image_url
            location = place.get('location', '')
            if location:
                address = location.get('display_address', '')
                place['address'] = address
            else:
                place['address'] = 'No address available'
            places_to_display.append(place)
        if places_to_display:
            return { 'status': 'success', 'code': 200, 'message': 'OK', 'places': places_to_display }
        else:
            return { 'status': 'error', 'code': 204, 'message': 'Yelp could not find any results' }
    else:
        return { 'status': 'error', 'code': 404, 'message': 'Could not get Yelp data, server does not respond.' }