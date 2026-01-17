from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.domain.models.chunk import Chunk

class VectorStore(ABC):
    """Abstract base class for Vector Store operations."""

    @abstractmethod
    async def add_chunks(self, chunks: List[Chunk]) -> bool:
        """Add chunks to the vector store."""
        pass

    @abstractmethod
    async def search(self, query_embedding: List[float], k: int = 5) -> List[Chunk]:
        """Search for similar chunks."""
        pass
    
    @abstractmethod
    async def delete_document_chunks(self, document_id: str) -> bool:
        """Delete all chunks for a specific document."""
        pass
