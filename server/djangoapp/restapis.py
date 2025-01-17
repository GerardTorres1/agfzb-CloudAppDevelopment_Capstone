import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import NaturalLanguageUnderstandingV1, Features, SentimentOptions, CategoriesOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        # dealers = json_result["rows"]
        # For each dealer object
        for dealer in json_result:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_by_id(url, id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=id)
    if json_result:
        # Get the row list in JSON as dealers
        # dealers = json_result["rows"]
        # For each dealer object
        for dealer in json_result:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
            print(dealer_doc["full_name"])
    return results


def get_dealer_reviews_from_cf(url, dealerId):
    # Construye la URL completa aquí
    """ full_url = url + '?id=' + str(dealerId)
    print(full_url) """
    results = []
    # Call get_request with a URL parameter
    # json_result = get_request(url, dealerId=dealerId)
    json_result = get_request(url, id=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        # dealers = json_result["rows"]
        # For each dealer object
        for review in json_result["data"]["docs"]:
            # Get its content in `doc` object
            review_doc = review
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"],
                                      purchase=review_doc["purchase"], review=review_doc["review"],
                                      purchase_date=review_doc["purchase_date"], car_make=review_doc["car_make"],
                                      car_model=review_doc["car_model"], car_year=review_doc["car_year"],
                                      sentiment=None, id=review_doc["id"])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative


def analyze_review_sentiments(dealerreview):
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/eabf5d48-b897-4067-9d77-0f49d09de335"
    api_key = "IhzBSNJ3qVHHBeaPLhNCh282wA26YIVB5Tw-O1F6Se1A"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07', authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(
        text=dealerreview,
        features=Features(sentiment=SentimentOptions(targets=[dealerreview]))).get_result()
    return response["sentiment"]["document"]["label"]


def post_request(url, json_payload, **kwargs):
    # print(kwargs)
    print("POST to {} ".format(url))
    print("JSON payload: {} ".format(json_payload))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, json=json_payload, params=kwargs)
        print(response)
        return response
    except:
        # If any error occurs
        print("Network exception occurred")
