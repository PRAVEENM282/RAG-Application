from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from app.core.dependencies import get_queue_service, get_file_store
from app.domain.ports.queue import QueueService
from app.infrastructure.storage.file_store import FileStore
from app.domain.models.document import Document
import shutil
import os

router = APIRouter()

@router.post("/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    queue: QueueService = Depends(get_queue_service),
    file_store: FileStore = Depends(get_file_store)
):
    try:
        # Save file contents
        content = await file.read()
        saved_path = await file_store.save_file(file.filename, content)

        # Create document record (in memory/db if we had one, for now just passing ID)
        doc = Document(
            filename=file.filename,
            content="", # We don't store full content in model here to save memory
            content_type=file.content_type,
            size=len(content)
        )

        # Push to queue
        message = {
            "document_id": doc.id,
            "filename": doc.filename,
            "file_path": saved_path
        }
        
        success = await queue.publish(message)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to queue document")

        return {"status": "queued", "document_id": doc.id, "filename": doc.filename}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
