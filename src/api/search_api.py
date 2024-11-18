# src/api/search_api.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

SERP_API_KEY = os.getenv("SERP_API_KEY")

def search_query(query):
    """
    Uses SerpAPI to perform a web search.
    
    Args:
        query (str): Search query string.

    Returns:
        dict: JSON response from SerpAPI containing search results.
    """
    base_url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERP_API_KEY
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching search results: {e}")
        return None
