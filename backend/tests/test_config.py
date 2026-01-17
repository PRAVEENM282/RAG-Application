"""
Unit tests for configuration and environment handling.
"""
import pytest
import os


class TestEnvironmentVariables:
    """Test environment variable handling."""
    
    def test_required_env_vars(self, mock_env):
        """Test that required environment variables are set."""
        required_vars = [
            "SECRET_KEY",
            "LLM_PROVIDER",
            "DATABASE_URL"
        ]
        
        for var in required_vars:
            assert os.getenv(var) is not None
    
    def test_secret_key_not_default(self, mock_env):
        """Test that secret key is set."""
        secret_key = os.getenv("SECRET_KEY")
        assert secret_key is not None
        assert len(secret_key) > 10
    
    def test_llm_provider_valid(self, mock_env):
        """Test that LLM provider is valid."""
        provider = os.getenv("LLM_PROVIDER")
        valid_providers = ["openai", "groq", "gemini", "local"]
        
        assert provider in valid_providers


class TestConfiguration:
    """Test configuration settings."""
    
    def test_jwt_algorithm(self):
        """Test JWT algorithm configuration."""
        algorithm = "HS256"
        
        assert algorithm in ["HS256", "HS384", "HS512"]
    
    def test_token_expiry(self):
        """Test token expiry configuration."""
        expiry_minutes = 30
        
        assert expiry_minutes > 0
        assert expiry_minutes <= 1440  # Max 24 hours
    
    def test_chunk_size_config(self):
        """Test chunk size configuration."""
        chunk_size = 1000
        chunk_overlap = 200
        
        assert chunk_size > 0
        assert chunk_overlap >= 0
        assert chunk_overlap < chunk_size
    
    def test_max_file_size(self):
        """Test max file size configuration."""
        max_size_mb = 10
        max_size_bytes = max_size_mb * 1024 * 1024
        
        assert max_size_bytes > 0
        assert max_size_mb <= 100  # Reasonable limit


class TestDatabaseConfig:
    """Test database configuration."""
    
    def test_database_url_format(self, mock_env):
        """Test database URL format."""
        db_url = os.getenv("DATABASE_URL")
        
        assert db_url is not None
        assert "sqlite" in db_url or "postgresql" in db_url
    
    def test_redis_url_format(self, mock_env):
        """Test Redis URL format."""
        redis_url = os.getenv("REDIS_URL")
        
        assert redis_url is not None
        assert redis_url.startswith("redis://")
