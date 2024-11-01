import openai
from typing import List, Dict

class LLMAnalyzer:
    def __init__(self, api_key: str, model: str = "gpt-4", max_tokens: int = 2048):
        """
        Initializes the LLMAnalyzer with API key and model details.
        
        Args:
            api_key (str): The API key for OpenAI.
            model (str): The model to use (e.g., "gpt-4").
            max_tokens (int): Maximum tokens to use per request.
        """
        self.api_key = api_key
        openai.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens

    def get_response(self, prompt: str) -> str:
        """
        Sends a prompt to the LLM and retrieves the response.
        
        Args:
            prompt (str): The prompt text for the LLM.
        
        Returns:
            str: The LLM's response text.
        """
        response = openai.Completion.create(
            model=self.model,
            prompt=prompt,
            max_tokens=self.max_tokens,
            temperature=0.7
        )
        return response.choices[0].text.strip()

    def summarize(self, text: str) -> str:
        """
        Summarizes the provided text.
        
        Args:
            text (str): The text to summarize.
        
        Returns:
            str: The summary of the text.
        """
        prompt = f"Summarize the following article:\n\n{text}\n\nSummary:"
        return self.get_response(prompt)

    def extract_key_points(self, text: str) -> List[str]:
        """
        Extracts key points from the text.
        
        Args:
            text (str): The text to extract key points from.
        
        Returns:
            List[str]: A list of key points.
        """
        prompt = f"List the key points from the following article:\n\n{text}\n\nKey Points:"
        response = self.get_response(prompt)
        return response.splitlines()  # Splitting by line in case LLM returns points line-by-line

    def analyze_sentiment(self, text: str) -> str:
        """
        Analyzes the sentiment of the text.
        
        Args:
            text (str): The text to analyze sentiment.
        
        Returns:
            str: The sentiment label (e.g., "Positive", "Neutral", "Negative").
        """
        prompt = f"Analyze the sentiment of the following text:\n\n{text}\n\nSentiment:"
        return self.get_response(prompt)

    def classify_topic(self, text: str) -> str:
        """
        Classifies the topic of the text.
        
        Args:
            text (str): The text to classify the topic.
        
        Returns:
            str: The identified topic label.
        """
        prompt = f"Identify the main topic of the following article:\n\n{text}\n\nTopic:"
        return self.get_response(prompt)
