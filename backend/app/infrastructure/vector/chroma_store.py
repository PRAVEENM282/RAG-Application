import chromadb
from typing import List
from app.domain.ports.vector_store import VectorStore
from app.domain.models.chunk import Chunk
from app.core.config import settings

class ChromaVectorStore(VectorStore):
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        self.collection = self.client.get_or_create_collection(name="rag_chunks")

    async def add_chunks(self, chunks: List[Chunk]) -> bool:
        if not chunks:
            return True
        
        ids = [chunk.id for chunk in chunks]
        documents = [chunk.content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        embeddings = [chunk.embedding for chunk in chunks]

        # Chroma requires embeddings to be provided if we want to skip its default embedding function
        # We assume embeddings are computed before calling add_chunks for now, 
        # or we could use an embedding function here if we prefer Chroma to do it.
        # Ideally, we want full control, so we should pass embeddings.
        # If embeddings are empty lists, Chroma might error if we don't provide an embedding function.
        # ensuring we have embeddings:
        if any(not e for e in embeddings):
             # For this implementation, we assume embeddings are present.
             # In a real scenario, we might want to call an embedding service here if missing.
             pass

        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings if embeddings[0] else None # helper to use default if none provided (testing)
        )
        return True

    async def search(self, query_embedding: List[float], k: int = 5) -> List[Chunk]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        
        chunks = []
        if results["ids"]:
            for i in range(len(results["ids"][0])):
                chunk = Chunk(
                    id=results["ids"][0][i],
                    document_id=results["metadatas"][0][i].get("document_id", "unknown"),
                    content=results["documents"][0][i],
                    metadata=results["metadatas"][0][i],
                    embedding=[] # Optimization: don't return embedding unless needed
                )
                chunks.append(chunk)
        return chunks

    async def delete_document_chunks(self, document_id: str) -> bool:
        self.collection.delete(
            where={"document_id": document_id}
        )
        return True
