import requests
from bs4 import BeautifulSoup

def handleRequests(query):
    try:
        response = requests.get(f'https://www.dictionary.com/browse/{query}').text
        return response
    except Exception:
        raise RuntimeError("Error occured while fetching data from the web, please try checking the internet connection.")

def getSoupObj(res):
    return BeautifulSoup(res, "html.parser")
