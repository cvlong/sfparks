import os
import requests
import json
from pprint import pprint
from flask import Flask, request, session, jsonify

client_id=os.environ['YELP_APP_ID']
client_secret=os.environ['YELP_APP_SECRET']


def get_yelp_token():


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


# def find_parks()
ACCESS_TOKEN = get_yelp_token()

url = "https://api.yelp.com/v3/businesses/search"

querystring = {'categories': 'parks',
               'location': '\"San Francisco\"'
    }

headers = {
    'authorization': "Bearer " + ACCESS_TOKEN,
    'cache-control': "no-cache",
    'postman-token': "02b8b64b-11d5-6248-217d-83a157c2e721"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

pprint(response.text)