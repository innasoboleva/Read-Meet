import requests, os
import urllib.parse # for URL encoding


# set up for yelp API requests
yelp_key = os.environ.get('YELP_KEY')
yelp_url = "https://api.yelp.com/v3/businesses/search?location={}&offset={}&term={}" # term is keyword as park or cafe, location can be address or zipcode


def _get_yelp_response(zipcode, type, page):
    """ Sending request to Yelp with required params """

    result_count = 20   # number of results from request
    offset = str(result_count * page)
    type_encoded = urllib.parse.quote(type)
    yelp_search_url_encoded = yelp_url.format(zipcode, offset, type_encoded)
    headers = {
            'Content-type': 'application/json',
            'Authorization': f'Bearer {yelp_key}',
        }
    print(yelp_search_url_encoded, headers)
    response_data = requests.get(yelp_search_url_encoded, headers=headers)
    response = response_data.json()
    return response
    

def _get_yelp_info_to_dict(response):
    """ From response get information and return in dict with places as key """

    if response.get("error") == None:
        places_to_display = []
        places = response.get('businesses', [])
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
        return { 'status': 'error', 'code': 404, 'message': 'Could not get Yelp data.' }
    

def find_places(zipcode, type, page=0):
    """
    Using Yelp API, method gets information for local businesses and returns a list of dictionaries with the result.
    Need zipcode and type of business to search for, park or cafe for example.
    """
    response = _get_yelp_response(zipcode, type, page)
    return _get_yelp_info_to_dict(response)