import requests
from typing import List, Dict, Optional
from src.utils import config

class NewsFetcher:
    def __init__(self, api_key: str = ""):
        """
        Initializes the NewsFetcher with the provided API key.
        
        Args:
            api_key (str): The API key for authenticating with the News API.
        """
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"
    
    def fetch_articles(self, query: str, from_date: Optional[str] = None, 
                       sort_by: str = "popularity", page_size: int = 10) -> List[Dict]:
        """
        Fetches articles based on a search query from the News API.
        
        Args:
            query (str): Search term for news articles.
            from_date (str, optional): Date to fetch articles from (in YYYY-MM-DD format).
            sort_by (str): Criteria for sorting results (e.g., 'popularity', 'relevancy').
            page_size (int): Number of articles to retrieve per request.
        
        Returns:
            List[Dict]: List of articles with title, date, description, content, source, and URL.
        """
        params = {
            "q": query,
            "from": from_date,
            "sortBy": sort_by,
            "pageSize": page_size,
            "apiKey": self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raises an error for bad HTTP status codes
            articles = response.json().get("articles", [])
            return [
                {
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                    "urlToImage": article.get("urlToImage"),
                    "publishedAt": article.get("publishedAt"),
                    "content": article.get("content"),
                    "source": article.get("source", {}).get("name")
                }
                for article in articles
            ]
        except requests.RequestException as e:
            print(f"Error fetching articles: {e}")
            return []        