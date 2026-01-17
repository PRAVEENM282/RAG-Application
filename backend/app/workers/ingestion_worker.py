import asyncio
import json
import logging
import os
from app.core.dependencies import get_queue_service, get_vector_store, get_file_store, get_embedding_service
from app.domain.models.chunk import Chunk
from app.domain.models.document import Document
# Simple text splitter placeholder
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pypdf

logger = logging.getLogger(__name__)

class IngestionWorker:
    def __init__(self):
        self.queue = get_queue_service()
        self.vector_store = get_vector_store()
        self.file_store = get_file_store()
        self.embedding_service = get_embedding_service()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

    def _extract_text_from_pdf(self, file_path: str) -> str:
        try:
            reader = pypdf.PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            logger.error(f"Failed to extract PDF text from {file_path}: {e}")
            raise e

    def _read_text_file(self, file_path: str) -> str:
        # Synchronous read for simplicity in this worker implementation, 
        # but since we are in a worker, blocking a thread is acceptable or we could use aiofiles
        # However, pypdf is blocking anyway.
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read text file {file_path}: {e}")
            raise e

    async def process_message(self, message: dict):
        logger.info(f"Processing message: {message}")
        try:
            filename = message.get("filename")
            file_path = message.get("file_path")
            document_id = message.get("document_id")

            if not file_path or not document_id:
                logger.error("Invalid message format")
                return

            # 1. Extract content based on file type
            content = ""
            if filename.lower().endswith(".pdf"):
                content = self._extract_text_from_pdf(file_path)
            else:
                content = self._read_text_file(file_path)
            
            if not content:
                logger.warning(f"No content extracted from {filename}")
                return

            # 2. Chunk text
            texts = self.text_splitter.split_text(content)
            
            # 3. Generate embeddings for all chunks (batch processing for efficiency)
            logger.info(f"Generating embeddings for {len(texts)} chunks")
            embeddings = self.embedding_service.embed_batch(texts)
            
            # 4. Create Chunks with real embeddings
            chunks = []
            for i, (text, embedding) in enumerate(zip(texts, embeddings)):
                chunk = Chunk(
                    document_id=document_id,
                    content=text,
                    embedding=embedding,
                    metadata={
                        "filename": filename,
                        "chunk_index": i
                    }
                )
                chunks.append(chunk)

            # 5. Store in Vector DB
            await self.vector_store.add_chunks(chunks)
            logger.info(f"Successfully processed document {filename} with {len(chunks)} chunks")

        except Exception as e:
            logger.error(f"Error processing document: {e}")

    async def run(self):
        await self.queue.consume(self.process_message)

if __name__ == "__main__":
    worker = IngestionWorker()
    asyncio.run(worker.run())
