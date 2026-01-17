from functools import lru_cache
from app.core.config import settings
from app.infrastructure.llm.factory import get_llm_provider
from app.infrastructure.vector.chroma_store import ChromaVectorStore
from app.infrastructure.queue.redis_queue import RedisQueue
from app.infrastructure.storage.file_store import FileStore
from app.infrastructure.embedding.embedding_service import EmbeddingService
from app.services.rag_service import RAGService
from app.services.context_builder import ContextBuilder

# Singletons
@lru_cache()
def get_vector_store():
    return ChromaVectorStore()

@lru_cache()
def get_queue_service():
    return RedisQueue()

@lru_cache()
def get_file_store():
    return FileStore()

@lru_cache()
def get_context_builder():
    return ContextBuilder()

@lru_cache()
def get_embedding_service():
    return EmbeddingService()

def get_rag_service():
    return RAGService(
        llm_provider=get_llm_provider(),
        vector_store=get_vector_store(),
        context_builder=get_context_builder(),
        embedding_service=get_embedding_service()
    )
