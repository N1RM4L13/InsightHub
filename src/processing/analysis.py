import datetime
from typing import List, Dict, Tuple
from collections import Counter, defaultdict
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class ArticleAnalyzer:
    def __init__(self, articles: List[Dict]):
        """
        Initializes the ArticleAnalyzer with a list of articles.
        
        Args:
            articles (List[Dict]): List of processed articles with fields like title, content, topic, and sentiment.
        """
        self.articles = articles

    def identify_trending_topics(self, top_n: int = 5) -> List[Tuple[str, int]]:
        """
        Identifies the trending topics by frequency.
        
        Args:
            top_n (int): Number of top trending topics to return.
        
        Returns:
            List[Tuple[str, int]]: List of top topics and their frequencies.
        """
        topics = [article['topic'] for article in self.articles if 'topic' in article]
        topic_counts = Counter(topics)
        trending_topics = topic_counts.most_common(top_n)
        return trending_topics

    def track_sentiment_over_time(self) -> Dict[str, Dict[str, int]]:
        """
        Tracks sentiment over time by date.
        
        Returns:
            Dict[str, Dict[str, int]]: A dictionary with dates as keys, and sentiment counts as values.
        """
        sentiment_by_date = defaultdict(lambda: Counter())
        for article in self.articles:
            date = article.get("publishedAt", "")
            sentiment = article.get("sentiment", "")
            if date and sentiment:
                date_str = date.split("T")[0]  # Extract only the date part
                sentiment_by_date[date_str][sentiment] += 1
        return dict(sentiment_by_date)

    def find_related_articles(self, target_article: Dict, top_n: int = 3) -> List[Dict]:
        """
        Finds articles related to a given target article based on content similarity.
        
        Args:
            target_article (Dict): The article for which to find related articles.
            top_n (int): Number of related articles to return.
        
        Returns:
            List[Dict]: List of related articles.
        """
        content_list = [article["content"] for article in self.articles]
        target_content = target_article["content"]
        
        # Vectorize contents for similarity measurement
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(content_list + [target_content])
        
        # Compute cosine similarity between target article and all other articles
        cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
        
        # Get indices of the most similar articles
        related_indices = cosine_similarities.argsort()[-top_n:][::-1]
        related_articles = [self.articles[idx] for idx in related_indices]
        return related_articles

    def generate_topic_clusters(self) -> Dict[str, List[Dict]]:
        """
        Generates clusters of articles by topic.
        
        Returns:
            Dict[str, List[Dict]]: A dictionary where keys are topics, and values are lists of articles for each topic.
        """
        clusters = defaultdict(list)
        for article in self.articles:
            topic = article.get("topic")
            if topic:
                clusters[topic].append(article)
        return dict(clusters)

# Usage Example
# Assuming `processed_articles` is a list of articles that includes 'topic' and 'sentiment' fields
# analyzer = ArticleAnalyzer(processed_articles)
# trending_topics = analyzer.identify_trending_topics()
# sentiment_over_time = analyzer.track_sentiment_over_time()
# related_articles = analyzer.find_related_articles(target_article=processed_articles[0])
# topic_clusters = analyzer.generate_topic_clusters()
