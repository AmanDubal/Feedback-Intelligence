import re
import string
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class TextPreprocessor:
    """Text preprocessing utilities for feedback analysis"""
    
    # Common stop words to remove
    STOP_WORDS = {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
        'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'or', 'that',
        'the', 'to', 'was', 'will', 'with', 'i', 'me', 'my', 'we', 'you',
        'app', 'application', 'update', 'bug', 'issue', 'problem', 'crash'
    }
    
    # Emoticon/emoji patterns
    EMOJI_PATTERN = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "]+", flags=re.UNICODE
    )
    
    # URL pattern
    URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')
    
    # Multiple spaces pattern
    SPACE_PATTERN = re.compile(r'\s+')
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = TextPreprocessor.URL_PATTERN.sub('', text)
        
        # Remove emojis
        text = TextPreprocessor.EMOJI_PATTERN.sub('', text)
        
        # Remove HTML tags if any
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\!\?]', '', text)
        
        # Remove multiple spaces
        text = TextPreprocessor.SPACE_PATTERN.sub(' ', text)
        
        # Strip whitespace
        text = text.strip()
        
        return text
    
    @staticmethod
    def tokenize(text: str) -> List[str]:
        """
        Tokenize text into words
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of tokens
        """
        # Split on whitespace and punctuation
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens
    
    @staticmethod
    def remove_stopwords(tokens: List[str]) -> List[str]:
        """
        Remove common stop words
        
        Args:
            tokens: List of tokens
            
        Returns:
            Filtered tokens
        """
        return [
            token for token in tokens 
            if token not in TextPreprocessor.STOP_WORDS and len(token) > 2
        ]
    
    @staticmethod
    def extract_keywords(text: str, num_keywords: int = 5) -> List[str]:
        """
        Extract important keywords from text
        
        Args:
            text: Text to extract from
            num_keywords: Number of keywords to extract
            
        Returns:
            List of keywords
        """
        # Clean and tokenize
        cleaned = TextPreprocessor.clean_text(text)
        tokens = TextPreprocessor.tokenize(cleaned)
        
        # Remove stop words
        keywords = TextPreprocessor.remove_stopwords(tokens)
        
        # Simple frequency-based extraction
        from collections import Counter
        freq = Counter(keywords)
        
        # Get top N most frequent
        top_keywords = [word for word, _ in freq.most_common(num_keywords)]
        
        return top_keywords
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalize text for ML model input
        
        Args:
            text: Text to normalize
            
        Returns:
            Normalized text
        """
        # Clean
        text = TextPreprocessor.clean_text(text)
        
        # Remove multiple consecutive same characters (e.g., "soooo" -> "so")
        text = re.sub(r'(.)\1{2,}', r'\1', text)
        
        # Expand common contractions
        contractions = {
            "can't": "cannot",
            "won't": "will not",
            "don't": "do not",
            "doesn't": "does not",
            "didn't": "did not",
            "shouldn't": "should not",
            "wouldn't": "would not",
            "couldn't": "could not",
            "isn't": "is not",
            "aren't": "are not",
            "wasn't": "was not",
            "weren't": "were not",
            "hasn't": "has not",
            "haven't": "have not",
            "hadn't": "had not",
            "i'm": "i am",
            "you're": "you are",
            "he's": "he is",
            "she's": "she is",
            "it's": "it is",
            "we're": "we are",
            "they're": "they are",
            "i've": "i have",
            "you've": "you have",
            "we've": "we have",
            "they've": "they have",
            "i'll": "i will",
            "you'll": "you will",
            "he'll": "he will",
            "she'll": "she will",
            "it'll": "it will",
            "we'll": "we will",
            "they'll": "they will",
        }
        
        for contraction, expansion in contractions.items():
            text = re.sub(r'\b' + contraction + r'\b', expansion, text, flags=re.IGNORECASE)
        
        return text
    
    @staticmethod
    def detect_language(text: str) -> str:
        """
        Simple language detection based on common patterns
        
        Args:
            text: Text to detect language for
            
        Returns:
            Language code (e.g., 'en', 'es', 'fr')
        """
        # Very simple detection based on word patterns
        # In production, use a proper library like langdetect
        
        spanish_words = {'el', 'la', 'de', 'que', 'es', 'un', 'una', 'no'}
        french_words = {'le', 'la', 'de', 'que', 'est', 'un', 'une', 'pas'}
        german_words = {'der', 'die', 'das', 'den', 'von', 'und', 'ist', 'nicht'}
        
        tokens = set(TextPreprocessor.tokenize(text.lower()))
        
        spanish_count = len(tokens & spanish_words)
        french_count = len(tokens & french_words)
        german_count = len(tokens & german_words)
        
        if spanish_count > french_count and spanish_count > german_count:
            return 'es'
        elif french_count > german_count:
            return 'fr'
        elif german_count > 0:
            return 'de'
        else:
            return 'en'
    
    @staticmethod
    def extract_entities(text: str) -> Dict[str, List[str]]:
        """
        Extract potential entities like app versions, errors, etc.
        
        Args:
            text: Text to extract from
            
        Returns:
            Dictionary of entity types and their values
        """
        entities = {
            'versions': [],
            'errors': [],
            'platforms': [],
            'devices': []
        }
        
        text_lower = text.lower()
        
        # Version patterns (e.g., "v1.2.3" or "1.2.3")
        versions = re.findall(r'v?(\d+\.\d+(?:\.\d+)?)', text)
        entities['versions'] = list(set(versions))
        
        # Error patterns (e.g., "error", "crash", "fail")
        error_keywords = ['error', 'crash', 'fail', 'bug', 'freeze', 'hang', 'broken', 'exception', 'exception']
        for keyword in error_keywords:
            if keyword in text_lower:
                entities['errors'].append(keyword)
        
        # Platform detection
        platforms = ['ios', 'android', 'iphone', 'ipad', 'samsung', 'oneplus']
        for platform in platforms:
            if platform in text_lower:
                entities['platforms'].append(platform)
        
        # Device detection
        devices = ['iphone 12', 'iphone 13', 'iphone 14', 'galaxy s21', 'galaxy s22']
        for device in devices:
            if device in text_lower:
                entities['devices'].append(device)
        
        return entities
    
    @staticmethod
    def preprocess_for_clustering(text: str) -> str:
        """
        Preprocess text specifically for clustering algorithms
        
        Args:
            text: Text to preprocess
            
        Returns:
            Preprocessed text
        """
        # Normalize
        text = TextPreprocessor.normalize_text(text)
        
        # Tokenize and remove stopwords
        tokens = TextPreprocessor.tokenize(text)
        tokens = TextPreprocessor.remove_stopwords(tokens)
        
        # Rejoin
        return ' '.join(tokens)
