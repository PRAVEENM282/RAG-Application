from datetime import datetime
from uuid import uuid4
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class Document(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    filename: str
    content: str
    content_type: str
    size: int
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    processed: bool = False

class DocumentUpload(BaseModel):
    filename: str
    content_type: str
    file_path: str
