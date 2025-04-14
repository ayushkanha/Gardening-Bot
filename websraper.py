from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()
SECRAPER_API_KEY = os.getenv("SECRAPER_API_KEY")
def ws(name):
    params = {
    "engine": "google_shopping",
    "q": name,
    "api_key": SECRAPER_API_KEY,
    "gl" : "in"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results["shopping_results"]
    return(shopping_results[0:10])