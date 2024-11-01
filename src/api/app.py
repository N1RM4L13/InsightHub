from fastapi import FastAPI, HTTPException, Depends, Query
from typing import List, Dict
from datetime import datetime, timedelta
from pydantic import BaseModel
from collections import defaultdict

# Import necessary classes from other modules
from src.data.fetch_data import NewsFetcher
from src.processing.article_processor import ArticleProcessor
from src.analysis.llm_analyzer import LLMAnalyzer

# Initialize FastAPI app in api/app.py
app = FastAPI()

# Instantiate necessary classes
news_fetcher = NewsFetcher(api_key="your_newsapi_key_here")
article_processor = ArticleProcessor()
analyzer = LLMAnalyzer(api_key="your_openai_key_here")

# In-memory rate limiter
rate_limit_store = defaultdict(lambda: {"last_access": None, "request_count": 0})
RATE_LIMIT = 10  # Max requests per minute
RATE_LIMIT_RESET_TIME = timedelta(minutes=1)

class ArticleQuery(BaseModel):
    query: str
    from_date: str = Query(None, description="Date in YYYY-MM-DD format to start fetching articles from.")
    sort_by: str = Query("popularity", description="Criteria for sorting articles (e.g., popularity).")
    page_size: int = Query(10, description="Number of articles to return.")

def rate_limit(ip: str):
    """
    Simple in-memory rate limiting based on IP.
    """
    user_data = rate_limit_store[ip]
    current_time = datetime.now()
    
    # Reset rate limit after the defined reset time
    if user_data["last_access"] is None or current_time - user_data["last_access"] > RATE_LIMIT_RESET_TIME:
        user_data["request_count"] = 0
        user_data["last_access"] = current_time

    # Check if rate limit exceeded
    if user_data["request_count"] >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    
    user_data["request_count"] += 1
    user_data["last_access"] = current_time

@app.get("/search_articles", summary="Search Articles", description="Fetches and processes news articles based on a search query.")
async def search_articles(
    article_query: ArticleQuery,
    client_ip: str = Depends(lambda: "127.0.0.1")  # Placeholder IP, replace with logic to get client IP
) -> List[Dict]:
    """
    Endpoint to search for articles, process them, and return the results.
    
    Args:
        article_query (ArticleQuery): The search query, date, sort method, and page size.
    
    Returns:
        List[Dict]: Processed and analyzed articles.
    """
    # Apply rate limiting
    rate_limit(client_ip)
    
    # Fetch articles
    articles = news_fetcher.fetch_articles(
        query=article_query.query,
        from_date=article_query.from_date,
        sort_by=article_query.sort_by,
        page_size=article_query.page_size
    )

    # Process articles
    processed_articles = article_processor.process_articles(articles)
    
    # Analyze each article
    analyzed_articles = []
    for article in processed_articles:
        article_summary = analyzer.summarize(article['content'])
        article_key_points = analyzer.extract_key_points(article['content'])
        article_sentiment = analyzer.analyze_sentiment(article['content'])
        article_topic = analyzer.classify_topic(article['content'])

        analyzed_article = {
            "title": article["title"],
            "summary": article_summary,
            "key_points": article_key_points,
            "sentiment": article_sentiment,
            "topic": article_topic,
            "publishedAt": article["publishedAt"],
            "source": article["source"]
        }
        analyzed_articles.append(analyzed_article)
    
    return analyzed_articles
