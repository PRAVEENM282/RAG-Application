from uuid import uuid4
from typing import Dict, Any, List
from pydantic import BaseModel, Field

class Chunk(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    document_id: str
    content: str
    embedding: List[float] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    page_number: int = 0
    chunk_index: int = 0
