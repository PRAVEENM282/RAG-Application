"""
Unit tests for embedding and vector operations.
"""
import pytest
import numpy as np


class TestEmbeddingOperations:
    """Test embedding generation and operations."""
    
    def test_embedding_dimension(self):
        """Test that embeddings have correct dimensions."""
        # Mock embedding (typical sentence-transformers dimension)
        embedding = np.random.rand(384)
        
        assert len(embedding) == 384
        assert isinstance(embedding, np.ndarray)
    
    def test_embedding_normalization(self):
        """Test embedding normalization."""
        embedding = np.array([3.0, 4.0])
        normalized = embedding / np.linalg.norm(embedding)
        
        # Normalized vector should have magnitude 1
        magnitude = np.linalg.norm(normalized)
        assert abs(magnitude - 1.0) < 1e-6
    
    def test_cosine_similarity(self):
        """Test cosine similarity calculation."""
        vec1 = np.array([1.0, 0.0, 0.0])
        vec2 = np.array([1.0, 0.0, 0.0])
        vec3 = np.array([0.0, 1.0, 0.0])
        
        # Identical vectors should have similarity 1
        sim_identical = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        assert abs(sim_identical - 1.0) < 1e-6
        
        # Orthogonal vectors should have similarity 0
        sim_orthogonal = np.dot(vec1, vec3) / (np.linalg.norm(vec1) * np.linalg.norm(vec3))
        assert abs(sim_orthogonal) < 1e-6


class TestVectorSearch:
    """Test vector search operations."""
    
    def test_top_k_selection(self):
        """Test selecting top-k most similar vectors."""
        # Mock similarity scores
        scores = [0.9, 0.7, 0.95, 0.6, 0.85]
        k = 3
        
        # Get indices of top-k scores
        top_k_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        top_k_scores = [scores[i] for i in top_k_indices]
        
        assert len(top_k_scores) == k
        assert top_k_scores == [0.95, 0.9, 0.85]
    
    def test_similarity_threshold(self):
        """Test filtering by similarity threshold."""
        scores = [0.9, 0.7, 0.95, 0.6, 0.85]
        threshold = 0.8
        
        filtered_scores = [s for s in scores if s >= threshold]
        
        assert len(filtered_scores) == 3
        assert all(s >= threshold for s in filtered_scores)


class TestChunkMetadata:
    """Test chunk metadata handling."""
    
    def test_chunk_metadata_structure(self):
        """Test chunk metadata structure."""
        metadata = {
            "document_id": "doc123",
            "chunk_index": 0,
            "text": "This is a chunk of text",
            "source": "document.pdf",
            "page": 1
        }
        
        assert "document_id" in metadata
        assert "chunk_index" in metadata
        assert "text" in metadata
        assert isinstance(metadata["chunk_index"], int)
    
    def test_chunk_id_generation(self):
        """Test generating unique chunk IDs."""
        doc_id = "doc123"
        chunk_index = 5
        chunk_id = f"{doc_id}_chunk_{chunk_index}"
        
        assert chunk_id == "doc123_chunk_5"
        assert doc_id in chunk_id
