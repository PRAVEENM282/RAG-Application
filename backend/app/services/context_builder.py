from typing import List
from app.domain.models.chunk import Chunk

class ContextBuilder:
    def build_context(self, chunks: List[Chunk]) -> str:
        context_parts = []
        for i, chunk in enumerate(chunks):
            context_parts.append(f"Source {i+1} ({chunk.metadata.get('filename', 'unknown')}): {chunk.content}")
        
        return "\n\n".join(context_parts)
