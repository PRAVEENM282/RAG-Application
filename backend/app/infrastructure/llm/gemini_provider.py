from typing import AsyncGenerator
import google.generativeai as genai
from app.domain.ports.llm_provider import LLMProvider
from app.core.config import settings

class GeminiProvider(LLMProvider):
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    async def generate_stream(self, prompt: str, system_prompt: str = "") -> AsyncGenerator[str, None]:
        # Gemini handling of system prompts is a bit different, but we'll prepend for now or use specific API features
        # For simplicity, prepending system prompt if supported or just mixing (Gemini Pro supports system instructions separately now, but keeping simple)
        full_prompt = prompt
        if system_prompt:
            # Note: A better way with newer SDK is to pass system instruction in model creation, 
            # but that requires re-instantiation or checking SDK version. 
            # We will just prepend for this implementation.
            full_prompt = f"System: {system_prompt}\nUser: {prompt}"

        response = await self.model.generate_content_async(full_prompt, stream=True)
        
        async for chunk in response:
            if chunk.text:
                yield chunk.text

    def get_provider_name(self) -> str:
        return "gemini"
