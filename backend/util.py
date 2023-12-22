import requests
from openai import OpenAI
import os
import sqlite3


#get api keys from env file
google_api_key = os.environ.get("GOOGLE_API_KEY")
openai_api_key = os.environ.get("OPENAI_API_KEY")

conn = sqlite3.connect('reviews.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS review_summaries (
    id TEXT PRIMARY KEY,
    review_summary TEXT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP
)''')


#get nearby restaurants
def get_nearby_restaurants(location,tag, radius=200, keyword='restaurant', num_results=5):
    '''
    Returns the restaurants from the API call based on location, radius
    @
    '''
    base_url = 'https://maps.googleapis.com/maps/api/place/'
    
    # search for restaurants without specify the kind of restaurants
    if not tag :
        params = {
            'location': location,
            'radius': radius,
            'keyword': keyword,
            'key': google_api_key
        }
        response = requests.get(base_url+'nearbysearch/json', params=params)
    else:
        params = {
            'location': location,
            'radius': radius,
            'query': tag,
            'key': google_api_key
        } 
        response = requests.get(base_url+'textsearch/json', params=params)

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

    return summary

def fetch_review(place_id):
    cursor.execute('SELECT * FROM review_summaries WHERE id = ?', (place_id,))
    return cursor.fetchall()

def get_summary(place_id):
    review_array = fetch_review(place_id)

    if len(review_array) > 0:
        review = review_array[0]
        summary = review[1]
    else:
        reviews = get_place_details(place_id).get('reviews', [])
        summary = generate_summary(OpenAI(), reviews)
        cursor.execute('INSERT INTO review_summaries (id, review_summary) VALUES (?, ?)', (place_id, summary))
        conn.commit()

    return summary

def get_all_summaries(restaurants):
    summaries = []
    for restaurant in restaurants:
        summaries.append(get_summary(restaurant['place_id']))

    return summaries