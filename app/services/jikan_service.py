#app/services/jikan_services.py
import requests
import time
from typing import Optional, Dict, List

class JikanService:
    BASE_URL = 'https://api.jikan.moe/v4'
    RATE_LIMIT_DELAY = 0.4 # 400ms delay between requests.
    @staticmethod
    def _make_request(endpoint: str) -> Optional[Dict]:
        """
        Make a request to Jikan API with rate limiting 

        Args: 
            endpoint (str): API endpoint (e.g., '/anime/1')

        Returns: 
            Optional[Dict]: JSON reponse or None if error
        """
        
        try:
            time.sleep(JikanService.RATE_LIMIT_DELAY)
            url = f'{JikanService.BASE_URL}{endpoint}'
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Jikan API Error: {e}")
            return None
        
    
    @staticmethod
    def search_anime(query: str, limit: int = 20) -> List[Dict]:
        """
        Search for anime by title
        
        Args: 
            query (str) : Search query (anime title)
            limit (int) : Maximum number of results (default:20)

        Returns:
            List[Dict]: List of naime results
        """

        if not query or not query.strip():
            return []
        endpoint = f'/anime?q={query}&limit={limit}'
        response = JikanService._make_request(endpoint)
        if response and 'data' in response:
            return response['data']
        
        return[]
    