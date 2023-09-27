from apis import yelp_api

class TestYelpApi:
    # Mock data, search arg provided and key provided
    respond1 = {
    "businesses": [
        {
            "id": "sOw4N7nYJAqaTGN3ay_rJQ",
            "alias": "san-ramon-central-park-san-ramon",
            "name": "San Ramon Central Park",
            "image_url": "https://s3-media2.fl.yelpcdn.com/bphoto/Y2FjANJqdkM7zOV7O4ghRw/o.jpg",
            "is_closed": False,
            "url": "https://www.yelp.com/biz/san-ramon-central-park-san-ramon?adjust_creative=QOdVY7n8fwgZJfCXW4x8fg&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=QOdVY7n8fwgZJfCXW4x8fg",
            "review_count": 102,
            "categories": [
                {
                    "alias": "parks",
                    "title": "Parks"
                },
                {
                    "alias": "communitycenters",
                    "title": "Community Centers"
                }
            ],
            "rating": 4.5,
            "coordinates": {
                "latitude": 37.7658972144127,
                "longitude": -121.95224404335
            },
            "transactions": [],
            "location": {
                "address1": "12501 Alcosta Blvd",
                "address2": "",
                "address3": "",
                "city": "San Ramon",
                "zip_code": "94583",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "12501 Alcosta Blvd",
                    "San Ramon, CA 94583"
                ]
            },
            "phone": "+19259733200",
            "display_phone": "(925) 973-3200",
            "distance": 2667.8102892393817
        },
        {
            "id": "KIZkAp8SpT3hU8xtLwLEOQ",
            "alias": "rancho-san-ramon-community-park-san-ramon",
            "name": "Rancho San Ramon Community Park",
            "image_url": "https://s3-media4.fl.yelpcdn.com/bphoto/LcLBxcBUvg_kc-4z1ieU8g/o.jpg",
            "is_closed": False,
            "url": "https://www.yelp.com/biz/rancho-san-ramon-community-park-san-ramon?adjust_creative=QOdVY7n8fwgZJfCXW4x8fg&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=QOdVY7n8fwgZJfCXW4x8fg",
            "review_count": 101,
            "categories": [
                {
                    "alias": "parks",
                    "title": "Parks"
                }
            ],
            "rating": 4.5,
            "coordinates": {
                "latitude": 37.749738,
                "longitude": -121.919221
            },
            "transactions": [],
            "location": {
                "address1": "2000 Rancho Park Loop Rd",
                "address2": "",
                "address3": "",
                "city": "San Ramon",
                "zip_code": "94582",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "2000 Rancho Park Loop Rd",
                    "San Ramon, CA 94582"
                ]
            },
            "phone": "+19259733200",
            "display_phone": "(925) 973-3200",
            "distance": 6020.017743107041
        },
        {
            "id": "eILUhwSGVhsGVisvxTvDUw",
            "alias": "athan-downs-park-san-ramon-2",
            "name": "Athan Downs Park",
            "image_url": "https://s3-media4.fl.yelpcdn.com/bphoto/em-cGy6ZUFGOyaRLIbzuyg/o.jpg",
            "is_closed": False,
            "url": "https://www.yelp.com/biz/athan-downs-park-san-ramon-2?adjust_creative=QOdVY7n8fwgZJfCXW4x8fg&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=QOdVY7n8fwgZJfCXW4x8fg",
            "review_count": 48,
            "categories": [
                {
                    "alias": "parks",
                    "title": "Parks"
                },
                {
                    "alias": "playgrounds",
                    "title": "Playgrounds"
                },
                {
                    "alias": "tennis",
                    "title": "Tennis"
                }
            ],
            "rating": 5.0,
            "coordinates": {
                "latitude": 37.7478110790253,
                "longitude": -121.95641823113
            },
            "transactions": [],
            "location": {
                "address1": "2975 Montevideo Dr",
                "address2": "",
                "address3": "",
                "city": "San Ramon",
                "zip_code": "94583",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "2975 Montevideo Dr",
                    "San Ramon, CA 94583"
                ]
            },
            "phone": "+19259732817",
            "display_phone": "(925) 973-2817",
            "distance": 3253.1579245419202
        },

        ],
        "total": 377,
        "region": {
            "center": {
                "longitude": -121.98394775390625,
                "latitude": 37.767413217936834
            }
        }
    }
    # Mock data with error
    respond2 = {
    "error": {
        "code": "VALIDATION_ERROR",
        "description": "Please specify a location or a latitude and longitude"
        }
    }
    # Mock data - empty
    respond3 = {}

    def test_get_yelp_info_to_dict_1(self):
        """ Checking that yelp response is valid with error status """
        places_to_display = [
            {
                "id": "sOw4N7nYJAqaTGN3ay_rJQ", "url": "https://www.yelp.com/biz/san-ramon-central-park-san-ramon?adjust_creative=QOdVY7n8fwgZJfCXW4x8fg&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=QOdVY7n8fwgZJfCXW4x8fg",\
                      "name": "San Ramon Central Park", "image": "https://s3-media2.fl.yelpcdn.com/bphoto/Y2FjANJqdkM7zOV7O4ghRw/o.jpg", \
                        "address": "12501 Alcosta Blvd, San Ramon, CA 94583", "rating": 4.5
            },
            {
                "id": "KIZkAp8SpT3hU8xtLwLEOQ", "url": "https://www.yelp.com/biz/rancho-san-ramon-community-park-san-ramon?adjust_creative=QOdVY7n8fwgZJfCXW4x8fg&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=QOdVY7n8fwgZJfCXW4x8fg", \
                    "name": "Rancho San Ramon Community Park", "image": "https://s3-media4.fl.yelpcdn.com/bphoto/LcLBxcBUvg_kc-4z1ieU8g/o.jpg", \
                        "address": "2000 Rancho Park Loop Rd, San Ramon, CA 94582", "rating": 4.5
            },
            {
                "id": "eILUhwSGVhsGVisvxTvDUw", "url": "https://www.yelp.com/biz/athan-downs-park-san-ramon-2?adjust_creative=QOdVY7n8fwgZJfCXW4x8fg&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=QOdVY7n8fwgZJfCXW4x8fg", \
                    "name": "Athan Downs Park", "image": "https://s3-media4.fl.yelpcdn.com/bphoto/em-cGy6ZUFGOyaRLIbzuyg/o.jpg", \
                    "address": "2975 Montevideo Dr, San Ramon, CA 94583", "rating": 5.0
            }
            ]
        result = yelp_api._get_yelp_info_to_dict(self.respond1)
        assert result == { 'status': 'success', 'code': 200, 'message': 'OK', 'places': places_to_display } 


    def test_get_yelp_info_to_dict_2(self):
        """ Checking that yelp response is valid with success status """

        result = yelp_api._get_yelp_info_to_dict(self.respond2)
        assert result == { 'status': 'error', 'code': 404, 'message': 'Could not get Yelp data.' }


    def test_get_yelp_info_to_dict_2(self):
        """ Checking that yelp response is valid with empty data """

        result = yelp_api._get_yelp_info_to_dict(self.respond3)
        assert result == { 'status': 'error', 'code': 204, 'message': 'Yelp could not find any results' }
       