from app.core.config import settings
from app.domain.ports.llm_provider import LLMProvider
from app.infrastructure.llm.openai_provider import OpenAIProvider
from app.infrastructure.llm.groq_provider import GroqProvider
from app.infrastructure.llm.gemini_provider import GeminiProvider
from app.infrastructure.llm.local_provider import LocalProvider

def get_llm_provider() -> LLMProvider:
    provider_type = settings.LLM_PROVIDER
    
    if provider_type == "openai":
        return OpenAIProvider()
    elif provider_type == "groq":
        return GroqProvider()
    elif provider_type == "gemini":
        return GeminiProvider()
    elif provider_type == "local":
        return LocalProvider()
    else:
        raise ValueError(f"Unknown LLM provider: {provider_type}")
