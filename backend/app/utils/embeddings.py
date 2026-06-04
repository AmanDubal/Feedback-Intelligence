from typing import List, Optional, Dict, Any
import numpy as np
import logging
from sentence_transformers import SentenceTransformer
import openai
import google.generativeai as genai
from app.config import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for generating embeddings for text data"""
    
    def __init__(self, model_type: str = "sentence-transformers"):
        """
        Initialize embedding service
        
        Args:
            model_type: Type of embedding model ('sentence-transformers', 'openai', 'gemini')
        """
        self.model_type = model_type
        self.model = None
        self.openai_client = None
        self.gemini_model = None
        
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the appropriate embedding model"""
        try:
            if self.model_type == "sentence-transformers":
                # Use multi-lingual model for better performance
                self.model = SentenceTransformer(
                    'paraphrase-multilingual-mpnet-base-v2'
                )
                logger.info("Loaded Sentence Transformers model")
                
            elif self.model_type == "openai":
                openai.api_key = settings.OPENAI_API_KEY
                self.openai_client = openai.OpenAI()
                logger.info("Initialized OpenAI client")
                
            elif self.model_type == "gemini":
                genai.configure(api_key=settings.GOOGLE_AI_API_KEY)
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                logger.info("Initialized Gemini client")
                
        except Exception as e:
            logger.error(f"Error initializing embedding model: {e}")
            raise
    
    async def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding for a single text
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as list
        """
        if not text or not isinstance(text, str):
            return []
        
        try:
            if self.model_type == "sentence-transformers":
                embedding = self.model.encode(text, convert_to_numpy=True)
                return embedding.tolist()
                
            elif self.model_type == "openai":
                response = self.openai_client.embeddings.create(
                    model="text-embedding-3-small",
                    input=text
                )
                return response.data[0].embedding
                
            elif self.model_type == "gemini":
                # Gemini doesn't have direct embedding API, use text similarity instead
                # This is a workaround - for production, use proper API
                response = self.gemini_model.generate_content(
                    f"Convert to vector: {text[:500]}"
                )
                # Return placeholder - would need actual embedding API
                return [0.0] * 768
                
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    async def get_embeddings_batch(
        self,
        texts: List[str],
        batch_size: int = 32
    ) -> List[List[float]]:
        """
        Get embeddings for multiple texts
        
        Args:
            texts: List of texts to embed
            batch_size: Batch size for processing
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        embeddings = []
        
        try:
            if self.model_type == "sentence-transformers":
                # Process in batches for efficiency
                for i in range(0, len(texts), batch_size):
                    batch = texts[i:i + batch_size]
                    batch_embeddings = self.model.encode(
                        batch,
                        convert_to_numpy=True,
                        show_progress_bar=False
                    )
                    embeddings.extend(batch_embeddings.tolist())
                    
            elif self.model_type == "openai":
                # OpenAI allows batch processing
                response = self.openai_client.embeddings.create(
                    model="text-embedding-3-small",
                    input=texts
                )
                embeddings = [item.embedding for item in response.data]
                
            elif self.model_type == "gemini":
                # Fallback for Gemini
                for text in texts:
                    embedding = await self.get_embedding(text)
                    embeddings.append(embedding)
                    
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            raise
        
        return embeddings
    
    def get_similarity(
        self,
        embedding1: List[float],
        embedding2: List[float]
    ) -> float:
        """
        Calculate cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score between 0 and 1
        """
        try:
            arr1 = np.array(embedding1)
            arr2 = np.array(embedding2)
            
            # Cosine similarity
            similarity = np.dot(arr1, arr2) / (
                np.linalg.norm(arr1) * np.linalg.norm(arr2)
            )
            
            # Convert to 0-1 range
            return (similarity + 1) / 2
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def get_similarities_batch(
        self,
        embedding: List[float],
        embeddings: List[List[float]]
    ) -> List[float]:
        """
        Calculate similarities between one embedding and multiple embeddings
        
        Args:
            embedding: Reference embedding
            embeddings: List of embeddings to compare
            
        Returns:
            List of similarity scores
        """
        similarities = []
        for emb in embeddings:
            sim = self.get_similarity(embedding, emb)
            similarities.append(sim)
        return similarities
    
    def find_most_similar(
        self,
        embedding: List[float],
        embeddings: List[List[float]],
        top_k: int = 5
    ) -> List[int]:
        """
        Find indices of most similar embeddings
        
        Args:
            embedding: Reference embedding
            embeddings: List of embeddings to search
            top_k: Number of top results to return
            
        Returns:
            List of indices sorted by similarity (highest first)
        """
        similarities = self.get_similarities_batch(embedding, embeddings)
        
        # Get indices sorted by similarity (descending)
        indices = np.argsort(similarities)[::-1][:top_k]
        
        return indices.tolist()
    
    def dimension(self) -> int:
        """
        Get embedding dimension
        
        Returns:
            Dimensionality of embeddings
        """
        if self.model_type == "sentence-transformers":
            return self.model.get_sentence_embedding_dimension()
        elif self.model_type == "openai":
            return 1536  # text-embedding-3-small dimension
        elif self.model_type == "gemini":
            return 768  # placeholder
        return 768
    
    async def semantic_search(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search on documents
        
        Args:
            query: Search query
            documents: List of documents (must have 'content' or 'text' field)
            top_k: Number of results to return
            
        Returns:
            Top K most relevant documents
        """
        try:
            # Get query embedding
            query_embedding = await self.get_embedding(query)
            
            if not query_embedding:
                return []
            
            # Get document embeddings
            doc_texts = [
                doc.get('content', doc.get('text', ''))
                for doc in documents
            ]
            doc_embeddings = await self.get_embeddings_batch(doc_texts)
            
            if not doc_embeddings:
                return []
            
            # Find most similar
            indices = self.find_most_similar(
                query_embedding,
                doc_embeddings,
                top_k=top_k
            )
            
            # Return documents with scores
            results = []
            for idx in indices:
                sim = self.get_similarity(
                    query_embedding,
                    doc_embeddings[idx]
                )
                doc = documents[idx].copy()
                doc['similarity_score'] = sim
                results.append(doc)
            
            return results
            
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return []
    
    async def cluster_embeddings(
        self,
        embeddings: List[List[float]],
        num_clusters: int = 7,
        method: str = "kmeans"
    ) -> Dict[int, List[int]]:
        """
        Cluster embeddings
        
        Args:
            embeddings: List of embedding vectors
            num_clusters: Number of clusters
            method: Clustering method ('kmeans' or 'dbscan')
            
        Returns:
            Dictionary mapping cluster ID to document indices
        """
        try:
            from sklearn.cluster import KMeans, DBSCAN
            from sklearn.preprocessing import StandardScaler
            
            if not embeddings:
                return {}
            
            embeddings_array = np.array(embeddings)
            
            if method == "kmeans":
                clustering = KMeans(
                    n_clusters=num_clusters,
                    random_state=42,
                    n_init=10
                )
                labels = clustering.fit_predict(embeddings_array)
                
            else:  # DBSCAN
                scaler = StandardScaler()
                embeddings_scaled = scaler.fit_transform(embeddings_array)
                clustering = DBSCAN(eps=0.5, min_samples=2)
                labels = clustering.fit_predict(embeddings_scaled)
            
            # Group by cluster
            clusters = {}
            for idx, label in enumerate(labels):
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(idx)
            
            return clusters
            
        except Exception as e:
            logger.error(f"Error clustering embeddings: {e}")
            return {}
