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
from util import get_nearby_restaurants, get_place_details, generate_summary
from openai import OpenAI

api_key = "#######"
base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

app = Flask(__name__)

@app.route("/")
def root():
    return jsonify({
        'version': '0.1.0',
        'description': 'This API give you the results of the best restaurants in your location.'
    })


@app.route("/find", methods=['GET'])
def find_restaurants():

    print("calling endpoint")
    client = OpenAI()

    try:

        print("extracting url params")
        lat = request.args.get('lat')
        lng = request.args.get('lon')


        # Parse coordinates into location
        location= '48.1363964,11.5609501'

        print("google api call")
        #You can adjust the radius, keyword, and num_results as needed
        restaurants = get_nearby_restaurants(location, radius=200, keyword='food', num_results=3) 

        #Initialize results list
        results = []

        print("restaurants: ", restaurants)

        for restaurant in restaurants:
                #Get place details 
                restaurant_id = restaurant.get('place_id')
                place_details = get_place_details(restaurant_id)

                #Get reviews for the place
                reviews = place_details.get('reviews', [])

                #Generate the summary
                summary = generate_summary(client, reviews)


                #Append restaurant details to results
                results.append({'name': place_details.get('name'),
                                'rating': place_details.get('rating'),
                                'summary': summary})
            
        # Return results as json
        return jsonify({'results': results})


    except Exception as e:
         return jsonify({'error': str(e)}), 500



@app.route("/test")
def test():

    test_var = request.args.get('test')

    return jsonify({'test': test_var
    })



if __name__ == '__main__':
    app.run(debug=True)