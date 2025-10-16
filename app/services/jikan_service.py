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
    def search_anime(query: str, page: int= 1, limit: int = 20) -> Dict:
        """
        Search for anime by title with pagination
        
        Args: 
            query (str) : Search query (anime title)
            page (int) : Page number (default: 1)
            limit (int) : Results per page (default:20)

        Returns:
            Dict: Contains 'results' (list) and 'has_next_page' (bool)
        """

        if not query or not query.strip():
            return {'results': [], 'has_next_page': False}
        
        endpoint = f'/anime?q={query}&page={page}&limit={limit}'
        response = JikanService._make_request(endpoint)

        if response and 'data' in response:
            # Check if there is a next page
            has_next_page = False
            if 'pagination' in response: 
                # Get 'has_next_page' value, default to false if not found.
                has_next_page = response['pagination'].get('has_next_page', False)


            return {
                'results': response['data'],
                'has_next_page': has_next_page,
                'current_page': page
            }
        
        return {'results': [], 'has_next_page': False}
    
    @staticmethod
    def get_anime_details(anime_id: int) -> Optional[Dict]:
        """
        Get detailed information about a specific anime

        Args:
            anime_id(int): MyAnimeList anime id

        Returns:
            Optional[Dict]: Anime Details or none if not found
        """

        endpoint = f'/anime/{anime_id}'
        response = JikanService._make_request(endpoint)

        if response and 'data' in response:
            return response['data']
        
        return None