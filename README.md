# iui-backend

## Set up the environment

Before starting the backend, ensure you have installed the necessary dependencies. You can do this by running the following command:

```bash
pip install -r requirements.txt
```

After installation, create a `.env` file at the root of this repository and populate it as follows:

```
GOOGLE_API_KEY=<YOUR_GOOGLE_API_KEY>
OPENAI_API_KEY=<YOUR_OPEN_AI_KEY>
```

## Starting the backend

To initiate the backend, navigate to the root of this project and execute the following command:

```bash
python backend/server.py
```

The backend will now be running on your localhost, accessible via port 5000.

To test the backend, visit the following URL: [http://127.0.0.1:5000/nearby_restaurants?lat=48.1363964&lng=11.5609501](http://127.0.0.1:5000/nearby_restaurants?lat=48.1363964&lng=11.5609501).
Simply modify the latitude and longitude parameters to scrape restaurants in different locations.

## Frontend

This backend serves as the supporting infrastructure for our `RestaurantFAInder` app, which can be found at: [https://github.com/FloKit/iui-frontend](https://github.com/FloKit/iui-frontend).

Make sure to clone the frontend repository and follow the instructions provided there for setup.
