'''
TODO: Create Google API Key, maybe every one have to create an own key and we have this api_key as environment variable
How to connect tto the google api?
Whats is requests (line 38)?
What is the output (format) of the get_nearby_restaurants? This is already a json? If not how can I get json?
start with impelmenting get_reviews

'''

from flask import Flask, jsonify
from markupsafe import escape

api_key = "#######"
base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

app = Flask(__name__)

@app.route("/")
def root():
    return jsonify({
        'version': '0.1.0',
        'description': 'This API give you the results of the best restaurants in your location.'
    })

@app.route("/restaurant/<string: location")
def get_restaurants(location):
    '''
    Returns the best restaurants in the user location as JSON. 
    '''
    return get_nearby_restaurants(location)

@app.route("/review/<string: restaurant_id>")
def get_reviews(restaurant_id):
    '''
    Return a recap of the review based on the selected restaurant given as restaurant_id
    '''
    return 'TODO'



def get_nearby_restaurants(location, radius=200, keyword='restaurant', num_results=5):
    '''
    Connect with the Google API, get the restaurants. 
    '''
    params = {
        'location': location,
        'radius': radius,
        'keyword': keyword,
        'key': api_key,
    }

    response = requests.get(base_url, params=params)
    results = response.json().get('results', [])

    results = results[:num_results]

    #return results

    return 'Work in progress'