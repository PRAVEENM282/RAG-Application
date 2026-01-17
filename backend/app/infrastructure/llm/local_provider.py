from typing import AsyncGenerator
import httpx
from app.domain.ports.llm_provider import LLMProvider
from app.core.config import settings

class LocalProvider(LLMProvider):
    def __init__(self):
        self.base_url = settings.LOCAL_LLM_URL
        self.model = "llama3" # Default local model

    async def generate_stream(self, prompt: str, system_prompt: str = "") -> AsyncGenerator[str, None]:
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "stream": True
        }
        
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", url, json=payload, timeout=None) as response:
                async for line in response.aiter_lines():
                    if line:
                        import json
                        try:
                            data = json.loads(line)
                            if "message" in data and "content" in data["message"]:
                                yield data["message"]["content"]
                        except:
                            pass

    def get_provider_name(self) -> str:
        return "local"
