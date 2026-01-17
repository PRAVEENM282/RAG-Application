"""
Unit tests for authentication functionality.
"""
import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext

# Constants from the app
SECRET_KEY = "CHANGE_THIS_IN_PROD_TO_A_REAL_SECRET_KEY"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TestPasswordHashing:
    """Test password hashing and verification."""
    
    def test_hash_password(self):
        """Test that passwords are hashed correctly."""
        password = "testpassword123"
        hashed = pwd_context.hash(password)
        
        assert hashed != password
        assert pwd_context.verify(password, hashed)
    
    def test_verify_wrong_password(self):
        """Test that wrong passwords fail verification."""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = pwd_context.hash(password)
        
        assert not pwd_context.verify(wrong_password, hashed)


class TestJWTTokens:
    """Test JWT token creation and validation."""
    
    def test_create_token(self):
        """Test JWT token creation."""
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        to_encode = {"exp": expire, "sub": "test_user"}
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        assert token is not None
        assert isinstance(token, str)
    
    def test_decode_valid_token(self):
        """Test decoding a valid JWT token."""
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        to_encode = {"exp": expire, "sub": "test_user"}
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        assert decoded["sub"] == "test_user"
        assert "exp" in decoded
    
    def test_decode_expired_token(self):
        """Test that expired tokens raise an error."""
        expire = datetime.now(timezone.utc) - timedelta(minutes=1)  # Already expired
        to_encode = {"exp": expire, "sub": "test_user"}
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        from jose import ExpiredSignatureError
        with pytest.raises(ExpiredSignatureError):
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    def test_decode_invalid_token(self):
        """Test that invalid tokens raise an error."""
        invalid_token = "invalid.token.here"
        
        from jose import JWTError
        with pytest.raises(JWTError):
            jwt.decode(invalid_token, SECRET_KEY, algorithms=[ALGORITHM])
