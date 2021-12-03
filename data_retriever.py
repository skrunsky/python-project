import urllib.request
import json

# Constants for the API calls (used in URL header field)
API_KEY = "4863dee5-509f-4b1e-978e-14656175524f"
HEADER_VAL = "x-messari-api-key"


def retrieve_currencies():
    # Placeholder dictionary to populate with data
    all_currencies = {}
    # Permanent URL for the API call to retrieve currencies
    request_url = "https://data.messari.io/api/v2/assets?fields=slug,name&limit=100"
    # Retrieve parsed JSON data
    currency_data = get_raw_data(request_url)
    # Ditch all the other stuff, and just read the currency slugs and names
    for item in currency_data:
        all_currencies[item["slug"]] = item["name"]
    # Return the new dictionary to populate UI
    return all_currencies


def get_market_data(currency, start_date, end_date):

    # Placeholder dictionary to populate with amazing data from API
    historical_data = {}
    # Create a beautiful query for the API call
    request_url = f"https://data.messari.io/api/v1/assets/" + currency + \
        "/metrics/price/time-series?start=" + start_date + \
        "&end=" + end_date + "&interval=1d&order=ascending"
    # Pull the raw JSON parsed data
    raw_data = get_raw_data(request_url)
    # Ditch all the other stuff, and just read the values
    retrieved_data = raw_data["data"]["values"]
    # Create the new dictionary with the time as key and closing price as value
    for item in retrieved_data:
        historical_data[item[0]] = item[4]
    # Return the new dictionary for further calculations
    return historical_data


def get_raw_data(url):
    # Open a new request with the given URL
    my_request = urllib.request.Request(url)
    # Fix the header fields, so we have access to the API
    my_request.add_header(HEADER_VAL, API_KEY)
    # Read all that juicy data
    raw_data = urllib.request.urlopen(my_request).read()
    # Let Python turn the json into something useful
    parsed_data = json.loads(raw_data)
    return parsed_data
