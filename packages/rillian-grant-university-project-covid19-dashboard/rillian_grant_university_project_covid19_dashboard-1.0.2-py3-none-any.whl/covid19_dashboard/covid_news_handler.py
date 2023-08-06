"""Function(s) for proforming newsapi calls and handling the results"""

import json
import requests

from .config import config

def news_api_request(search_terms="Covid COVID-19 coronavirus"):
    """Proforms a search query for articles with the given search terms
    Defaults to covid search terms
    """
    api_key = config["newsapi_key"]
    url = f"https://newsapi.org/v2/everything?q={search_terms}&apiKey={api_key}"
    res = requests.get(url)
    assert res.status_code == 200

    data = json.loads(res.content)

    return data
