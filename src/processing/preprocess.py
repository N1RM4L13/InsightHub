import re
from typing import Dict, List

class ArticleProcessor:
    def __init__(self):
        """
        Initializes the ArticleProcessor instance for processing and cleaning articles.
        """
        self.html_tags_pattern = re.compile(r'<.*?>')  # Regex for HTML tags
        self.special_chars_pattern = re.compile(r'[^A-Za-z0-9\s]')  # Regex for special characters

    def clean_text(self, text: str) -> str:
        """
        Cleans the text by removing HTML tags, special characters, and extra whitespace.
        
        Args:
            text (str): The original text to be cleaned.
        
        Returns:
            str: The cleaned text.
        """
        text = self.html_tags_pattern.sub('', text)  # Remove HTML tags
        text = self.special_chars_pattern.sub('', text)  # Remove special characters
        text = text.lower().strip()  # Convert to lowercase and trim whitespace
        return text

    def process_article(self, article: Dict) -> Dict:
        """
        Processes a single article by cleaning the content and extracting key information.
        
        Args:
            article (Dict): The article dictionary with fields like title, content, and date.
        
        Returns:
            Dict: A dictionary containing cleaned and processed article information.
        """
        # Only process the article if it has a non-empty description
        if not article.get("description"):
            return None  # Skip articles without a description
        
        processed_article = {
            "title": self.clean_text(article.get("title", "")),
            "description": self.clean_text(article.get("description", "")),
            "content": self.clean_text(article.get("content", "")),
            "publishedAt": article.get("publishedAt", ""),
            "source": article.get("source", {}).get("name", "")
        }
        return processed_article

    def process_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Processes a list of articles by cleaning each one and extracting key information.
        
        Args:
            articles (List[Dict]): List of articles to be processed.
        
        Returns:
            List[Dict]: List of processed articles with cleaned content, excluding any without a description.
        """
        processed_articles = [
            self.process_article(article) for article in articles if article.get("description")
        ]
        return [article for article in processed_articles if article is not None]

# Usage Example
# Assuming `articles` is a list of dictionaries fetched from NewsFetcher
# processor = ArticleProcessor()
# processed_articles = processor.process_articles(articles)
# print(processed_articles)
