from typing import AsyncGenerator
from app.domain.ports.llm_provider import LLMProvider
from app.domain.ports.vector_store import VectorStore
from app.services.context_builder import ContextBuilder
from app.infrastructure.embedding.embedding_service import EmbeddingService
from app.core.logging import logger

class RAGService:
    def __init__(
        self,
        llm_provider: LLMProvider,
        vector_store: VectorStore,
        context_builder: ContextBuilder,
        embedding_service: EmbeddingService
    ):
        self.llm_provider = llm_provider
        self.vector_store = vector_store
        self.context_builder = context_builder
        self.embedding_service = embedding_service

    async def query_stream(self, query: str) -> AsyncGenerator[dict, None]:
        # 1. Embed query using real embedding service
        logger.info(f"Embedding query: {query[:50]}...")
        query_embedding = self.embedding_service.embed_text(query)

        # 2. Retrieve relevant chunks
        chunks = await self.vector_store.search(query_embedding, k=3)
        
        # 3. Stream citations first (or parallel, but frontend expects them)
        for chunk in chunks:
            yield {
                "type": "citation",
                "payload": {
                    "source": chunk.metadata.get("filename", "unknown"),
                    "page": chunk.metadata.get("page", 1),
                    "text": chunk.content[:50] + "..."
                }
            }

        # 4. Build context
        context = self.context_builder.build_context(chunks)
        system_prompt = f"You are a helpful AI assistant. Use the following context to answer the user's question.\n\nContext:\n{context}"

        # 5. Stream LLM tokens
        try:
            async for token in self.llm_provider.generate_stream(query, system_prompt):
                yield {"type": "token", "payload": token}
        except Exception as e:
            logger.error(f"Error during LLM generation: {e}")
            yield {"type": "error", "payload": str(e)}

        yield {"type": "done", "payload": True}
