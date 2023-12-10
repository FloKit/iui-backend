import requests
from openai import OpenAI
import os


#get api keys from env file
google_api_key = os.environ.get("GOOGLE_API_KEY")
openai_api_key = os.environ.get("OPENAI_API_KEY")


#get nearby restaurants
def get_nearby_restaurants(location, radius=200, keyword='restaurant', num_results=5):
    '''
    Returns the restaurants from the API call based on location, radius
    '''
    base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    
    params = {
        'location': location,
        'radius': radius,
        'keyword': keyword,
        'key': google_api_key
    }
    
    response = requests.get(base_url, params=params)
    results = response.json().get('results', [])

    # Limit the number of results to the top 'num_results'
    results = results[:num_results]
    
    return results


def get_place_details(place_id):
    '''
    Returns details on a place defined by the place_id, e.g. reviews
    '''
    base_url = 'https://maps.googleapis.com/maps/api/place/details/json'

    params = {
        'place_id': place_id,
        'key': google_api_key
    }

    response = requests.get(base_url, params=params)
    result = response.json().get('result', {})

    return result


def generate_summary(client, reviews):
    #Concatenate all reviews
    review_text = "\n".join(review.get('text', '') for review in reviews)

    #Define the prompt for GPT
    prompt = f"Summarize the reviews for this place, please do not use more than 2-3 sentences: \n{review_text}"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ]
    )
    

    #Extract the generated summary from GPT's response
    summary = response.choices[0].message.content

    print("Summary: ", summary)

    return summary
    