import urllib.request
import json
import streamlit as st
import numpy as np
import pandas as pd

# Constants for the API calls (used in URL header field)
API_KEY = st.secrets["API_KEY"]
HEADER_VAL = "x-messari-api-key"

# DataRetriever class to fetch data using the Messari API


class DataRetriever:

    def __init__(self, api_key):
        self.API_KEY = api_key  # Initialize using the given API key

    def retrieve_currencies(self):
        # Placeholder dictionary to populate with data
        all_currencies = {}
        # Permanent URL for the API call to retrieve currencies
        # Defaulting to doing the 500 most popular currencies
        request_url = "https://data.messari.io/api/v1/assets?limit=500&fields=id,slug,symbol,metrics/market_data/price_usd"
        # Retrieve parsed JSON data
        currency_data = self.get_raw_data(request_url)
        # Ditch all the other stuff, and just read the currency slugs and names
        for item in currency_data["data"]:
            all_currencies[item["symbol"]] = item["slug"]
        # Return the new dictionary to populate UI
        return all_currencies

    def get_market_data(self, currency, start_date, end_date):
        # Placeholder list to populate with amazing data from API
        historical_data = []
        # Create a beautiful query for the API call
        request_url = f"https://data.messari.io/api/v1/assets/" + currency + \
            "/metrics/price/time-series?start=" + start_date + \
            "&end=" + end_date + "&interval=1d&order=ascending"
        # Pull the raw JSON parsed data
        raw_data = self.get_raw_data(request_url)
        # Ditch all the other stuff, and just read the values
        retrieved_data = raw_data["data"]["values"]
        # Create the new list with the time as key and closing price as value
        for item in retrieved_data:
            historical_data.append(item[4])
        # Conversions of data
        np_array = np.array(historical_data)  # Convert to numpy array
        # Convert to pandas dataframe
        my_dataframe = pd.DataFrame(np_array, columns=['close'])
        my_dataframe['returns'] = 100 * \
            np.log(my_dataframe['close']).diff()  # Calculate returns
        my_dataframe = my_dataframe['returns'].dropna()  # Drop NaN values
        returns = my_dataframe  # Change the naming of the dataframe
        # Return the dataframe for further calculations
        return returns

    def get_raw_data(self, url):
        # Open a new request with the given URL
        my_request = urllib.request.Request(url)
        # Fix the header fields, so we have access to the API
        my_request.add_header(HEADER_VAL, API_KEY)
        # Read all that juicy data
        raw_data = urllib.request.urlopen(my_request).read()
        # Let Python turn the json into something useful
        parsed_data = json.loads(raw_data)
        # Return the parsed data
        return parsed_data
