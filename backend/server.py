'''
TODO: Create Google API Key, maybe every one have to create an own key and we have this api_key as environment variable
How to connect to the google api?
Whats is requests (line 38)?
What is the output (format) of the get_nearby_restaurants? This is already a json? If not how can I get json?
start with impelmenting get_reviews

'''



'''
Final Goal: Single endpoint that checks restaurants nearby, picks 5, returns information with summarized Reviews

'''


from flask import Flask, jsonify, request
from markupsafe import escape
from util import get_nearby_restaurants, get_place_details, generate_summary, openai_api_key, get_summary, calculate_distance, get_photo_url
from openai import OpenAI
from dotenv import load_dotenv
import requests

api_key = "#######"
base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

app = Flask(__name__)

# enable environment variables 
load_dotenv()

@app.route("/")
def root():
    return jsonify({
        'version': '0.1.0',
        'description': 'This API give you the results of the best restaurants in your location.'
    })

@app.route("/nearby_restaurants", methods=['GET'])
def find_restaurants_nearby():
    '''
    Return resturans in your location.
    query:
        tag -- specify the kind of restaurant
        lag -- graphic latitude 
        lng -- graphic long
    '''

    try:

        # print("extracting url params")
        lat = request.args.get('lat')
        lng = request.args.get('lng')
        
        print("lat: ", lat)
        print("lng: ", lng)
        
        # lat = "48.1363964"
        # lng = "11.5609501"


        # Parse coordinates into location
        # location= '48.1363964,11.5609501'
        location= f'{lat},{lng}'

        # Type of restaurant
        tag = request.args.get('tag', None)

        #Get page
        page = int(request.args.get('page', '1'))

        #You can adjust the radius, keyword, and num_results as needed
        restaurants = get_nearby_restaurants(location=location, radius=1000, keyword='food', num_results=10, tag=tag, page=page)

        #Initialize results list
        results = []

        for restaurant in restaurants:
                #Get place details 
                restaurant_id = restaurant.get('place_id')
                place_details = get_place_details(restaurant_id)
                
                # check if place details  has photos
                if place_details.get('photos'):
                    photo_ref = place_details["photos"][0]["photo_reference"]
                    
                    photo_url = get_photo_url(photo_ref)
                    
                else:
                    photo_url= "https://www.shutterstock.com/image-vector/default-ui-image-placeholder-wireframes-600nw-1037719192.jpg"
                
                distance = calculate_distance(
                                float(lat),
                                float(lng), 
                                place_details.get('geometry').get('location').get('lat'),
                                place_details.get('geometry').get('location').get('lng'))

                #Append restaurant details to results
                results.append({'name': place_details.get('name'),
                                'rating': place_details.get('rating'),
                                'id': restaurant_id, 
                                'address': place_details.get('formatted_address',),
                                'total_ratings': place_details.get('user_ratings_total',),
                                'distance': distance, 
                                'image_url': photo_url})
            
        # Return results as json
        return jsonify({'results': results})


    except Exception as e:
         return jsonify({'error': str(e)}), 500


@app.route("/summary/<restaurant_id>")
def get_summary_for_restaurant(restaurant_id):
    '''
    Returns a summary of the reviews for a restaurant
    '''

    #Generate the summary
    summary = get_summary(restaurant_id)

    return jsonify({'summary': summary})



@app.route("/test")
def test():

    test_var = request.args.get('test')

    return jsonify({'test': test_var
    })



if __name__ == '__main__':
    app.run(debug=True)