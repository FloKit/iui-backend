import requests
from openai import OpenAI
import os
import sqlite3
from math import radians, sin, cos, sqrt, atan2


#get api keys from env file
google_api_key = os.environ.get("GOOGLE_API_KEY")
openai_api_key = os.environ.get("OPENAI_API_KEY")


#get nearby restaurants
def get_nearby_restaurants(location, radius=1000, keyword='restaurant', num_results=10, tag=None, page=1):
    '''
    Returns the restaurants from the API call based on location, radius
    @
    '''
    base_url = 'https://maps.googleapis.com/maps/api/place/'
    
    # search for restaurants without specify the kind of restaurants
    if not tag :
        params = {
            'location': location,
            # 'radius': radius,
            'keyword': keyword,
            'key': google_api_key,
            'rankby': 'distance'
        }
        response = requests.get(base_url+'nearbysearch/json', params=params)
    else:
        query = tag.replace(',', ' restaurant or ')

        params = {
            'location': location,
            'radius': radius,
            'query': query,
            'key': google_api_key
        } 
        response = requests.get(base_url+'textsearch/json', params=params)

    results = response.json().get('results', [])

    #Basic pagination
    page_results = num_results*page
    previous_page = num_results*(page-1)

    # Limit the number of results to the top 'num_results'
    results = results[previous_page:page_results]
  
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
    # prompt = f"Summarize the reviews for this place, please do not use more than 2-3 sentences: \n{review_text}"
    prompt = f"Please give me a summary of the reviews of this restaurant. I want one single summary for all 5 reviews. Please limit the summary to a maximum of 400 characters. It is extremely important that you limit the summary to a maximum of 400 characters: \n{review_text}"

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
    conn = sqlite3.connect('reviews.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS review_summaries (
        id TEXT PRIMARY KEY,
        review_summary TEXT,
        date DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    cursor.execute('SELECT * FROM review_summaries WHERE id = ?', (place_id,))
    res = cursor.fetchall()
    cursor.close()

    return res

def get_summary(place_id):
    review_array = fetch_review(place_id)

    if len(review_array) > 0:
        review = review_array[0]
        summary = review[1]
    else:
        reviews = get_place_details(place_id).get('reviews', [])
        summary = generate_summary(OpenAI(), reviews)
        try:
            conn = sqlite3.connect('reviews.db', check_same_thread=False)
            cursor = conn.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS review_summaries (
                id TEXT PRIMARY KEY,
                review_summary TEXT,
                date DATETIME DEFAULT CURRENT_TIMESTAMP
            )''')
            cursor.execute('DELETE FROM review_summaries WHERE id = ?', (place_id,))
            cursor.execute('INSERT INTO review_summaries (id, review_summary) VALUES (?, ?)', (place_id, summary))
            conn.commit()
        except sqlite3.ProgrammingError as e:
            print(e)
            print("this is the summary: ", summary)
            return summary
        finally:
            cursor.close()
        
    return summary


def get_all_summaries(restaurants):
    summaries = []
    for restaurant in restaurants:
        summaries.append(get_summary(restaurant['place_id']))

    return summaries

def calculate_distance(lat1, lon1, lat2, lon2):
    # Earth radius in meters
    earth_radius = 6371000  # in meters

    # Convert latitude and longitude from degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Calculate the change in coordinates
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    # Haversine formula
    a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate the distance
    distance = earth_radius * c
    return round(distance)

def get_photo_url(photo_ref):
    base_url = 'https://maps.googleapis.com/maps/api/place/photo'
    params = {
        'maxwidth': 400,
        'photoreference': photo_ref,
        'key': google_api_key
    }
    response = requests.get(base_url, params=params)
    
    return response.url