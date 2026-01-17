from abc import ABC, abstractmethod
from typing import Any, Callable, Awaitable

class QueueService(ABC):
    """Abstract base class for Queue operations."""

    @abstractmethod
    async def publish(self, message: dict) -> bool:
        """Publish a message to the queue."""
        pass

    @abstractmethod
    async def consume(self, callback: Callable[[dict], Awaitable[None]]) -> None:
        """Consume messages from the queue and trigger callback."""
        pass
