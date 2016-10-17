import os
import requests
import json
from pprint import pprint
from flask import Flask, request, session, jsonify

client_id=os.environ['YELP_APP_ID']
client_secret=os.environ['YELP_APP_SECRET']


def get_yelp_token():
    """Get secret token to use with Yelp API calls."""

    url = "https://api.yelp.com/oauth2/token"

    payload = {'client_id': client_id,
               'client_secret': client_secret,
               'grant_type': 'client_credentials'
        }

    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'cache-control': 'no-cache'
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    # print response.text

    ACCESS_TOKEN = json.loads(response.text)['access_token']
    return ACCESS_TOKEN


def get_image(name, latitude, longitude, address = None):
    """Find image URL using Yelp API."""

    ACCESS_TOKEN = get_yelp_token()

    url = "https://api.yelp.com/v3/businesses/search"

    querystring = {'term': name,
                   'location': address,
                   'latitude': latitude,
                   'longitude': longitude,
                   'categories': 'parks',
        }

    headers = {
        'authorization': "Bearer " + ACCESS_TOKEN,
        'cache-control': "no-cache",
        'postman-token': "02b8b64b-11d5-6248-217d-83a157c2e721"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    if json.loads(response.text)['businesses']:
        image = json.loads(response.text)['businesses'][0]['image_url']
    else:
        image = None
    
    return image
