import requests


#get nearby restaurants
def get_nearby_restaurants(api_key, location, radius=200, keyword='restaurant', num_results=5):
    '''
    Returns the restaurants from the API call based on location, radius
    
    '''
    base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    
    params = {
        'location': location,
        'radius': radius,
        'keyword': keyword,
        'key': api_key
    }
    
    response = requests.get(base_url, params=params)
    results = response.json().get('results', [])

    # Limit the number of results to the top 'num_results'
    results = results[:num_results]
    
    return results

def get_place_details(api_key, place_id):
    '''
    Returns details on a place defined by the place_id, e.g. reviews
    '''
    base_url = 'https://maps.googleapis.com/maps/api/place/details/json'

    params = {
        'place_id': place_id,
        'key': api_key
    }

    response = requests.get(base_url, params=params)
    result = response.json().get('result', {})

    return result

def generate_summary(reviews):
    """
    Calls the OpenAI API to generate a summary of reviews. reviews is passes as a list

    """

    #Concatenate all reviews
    review_text = "\n".join(review.get('text', '') for review in reviews)

    #Define the prompt for GPT
    prompt = f"Summarize the reviews for this place:\n{review_text}"

    #Generate short summary
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokes=100
    )

    #Extract the generated summary from GPT's response
    summary = response['choices'][0]['text'].strip()

    return summary