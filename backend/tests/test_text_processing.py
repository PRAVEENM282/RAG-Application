"""
Unit tests for text processing utilities.
"""
import pytest


class TestTextChunking:
    """Test text chunking functionality."""
    
    def test_chunk_text_basic(self):
        """Test basic text chunking."""
        text = "This is a test. " * 100  # Create a long text
        chunk_size = 100
        overlap = 20
        
        chunks = self._chunk_text(text, chunk_size, overlap)
        
        assert len(chunks) > 1
        for chunk in chunks:
            assert len(chunk) <= chunk_size + overlap
    
    def test_chunk_text_empty(self):
        """Test chunking empty text."""
        text = ""
        chunks = self._chunk_text(text, 100, 20)
        
        assert len(chunks) == 0 or (len(chunks) == 1 and chunks[0] == "")
    
    def test_chunk_text_short(self):
        """Test chunking text shorter than chunk size."""
        text = "Short text"
        chunks = self._chunk_text(text, 100, 20)
        
        assert len(chunks) == 1
        assert chunks[0] == text
    
    @staticmethod
    def _chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
        """Simple chunking implementation for testing."""
        if not text:
            return []
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - overlap
            
            if start >= len(text):
                break
        
        return chunks


class TestTextCleaning:
    """Test text cleaning utilities."""
    
    def test_remove_extra_whitespace(self):
        """Test removing extra whitespace."""
        text = "This  has   extra    spaces"
        cleaned = " ".join(text.split())
        
        assert cleaned == "This has extra spaces"
    
    def test_remove_newlines(self):
        """Test removing newlines."""
        text = "Line 1\nLine 2\nLine 3"
        cleaned = text.replace("\n", " ")
        
        assert "\n" not in cleaned
        assert "Line 1" in cleaned and "Line 2" in cleaned
    
    def test_strip_text(self):
        """Test stripping whitespace from text."""
        text = "  text with spaces  "
        cleaned = text.strip()
        
        assert cleaned == "text with spaces"


class TestDocumentMetadata:
    """Test document metadata extraction."""
    
    def test_extract_filename(self):
        """Test extracting filename from path."""
        path = "c:/users/test/documents/file.pdf"
        filename = path.split("/")[-1]
        
        assert filename == "file.pdf"
    
    def test_extract_file_extension(self):
        """Test extracting file extension."""
        filename = "document.pdf"
        extension = filename.split(".")[-1]
        
        assert extension == "pdf"
    
    def test_create_document_id(self):
        """Test creating document ID."""
        filename = "test_document.pdf"
        timestamp = "20260117"
        doc_id = f"{filename}_{timestamp}"
        
        assert doc_id == "test_document.pdf_20260117"
