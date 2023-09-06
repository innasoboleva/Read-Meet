import requests, os
import urllib.parse # for URL encoding


# set up for yelp API requests
yelp_key = os.environ.get('YELP_KEY')
yelp_url = "https://api.yelp.com/v3/businesses/search?location={}&term={}" # term is keyword as park or cafe, location can be address or zipcode

def find_places(zipcode, type, page=0):
    """
    Using Yelp API, method gets information for local businesses and returns a list of dictionaries with the result.
    Need zipcode and type of business to search for, park or cafe for example.
    """
    result_count = 20   # number of results from request
    offset = result_count * page
    type_encoded = urllib.parse.quote(type)
    # yelp_search_url = yelp_url.format(zipcode, type)
    yelp_search_url_encoded = yelp_url.format(zipcode, type_encoded)
    headers = {
            'Content-type': 'application/json',
            'Authorization': f'Bearer {yelp_key}',
            'offset': str(offset)
        }
    print(headers)
    response_data = requests.get(yelp_search_url_encoded, headers=headers)
    response = response_data.json()
    if response.get("error") == None:
        places_to_display = []
        places = response.get('businesses', [])
        print("PLACES length: ", len(places))
        for place in places:
            place_to_add = {}
            place_to_add["id"] = place.get("id")
            url = place.get('url', '')
            place_to_add['url'] = url
            name = place.get('name', '')
            place_to_add['name'] = name
            image_url = place.get('image_url', '')
            place_to_add['image'] = image_url
            location = place.get('location', '')
            if location:
                address = location.get('display_address', '')
                place_to_add['address'] = ", ".join(address)
            else:
                place_to_add['address'] = 'No address available'
            rating = place.get('rating', '')
            place_to_add['rating'] = rating
            places_to_display.append(place_to_add)
        if places_to_display:
            return { 'status': 'success', 'code': 200, 'message': 'OK', 'places': places_to_display }
        else:
            return { 'status': 'error', 'code': 204, 'message': 'Yelp could not find any results' }
    else:
        return { 'status': 'error', 'code': 404, 'message': 'Could not get Yelp data, server does not respond.' }