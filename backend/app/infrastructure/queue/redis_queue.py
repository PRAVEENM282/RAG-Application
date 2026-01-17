import json
import logging
import asyncio
from typing import Callable, Awaitable
from redis.asyncio import Redis
from app.domain.ports.queue import QueueService
from app.core.config import settings

logger = logging.getLogger(__name__)

class RedisQueue(QueueService):
    def __init__(self):
        self.redis = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )
        self.queue_name = settings.REDIS_QUEUE_NAME

    async def publish(self, message: dict) -> bool:
        try:
            await self.redis.rpush(self.queue_name, json.dumps(message))
            return True
        except Exception as e:
            logger.error(f"Failed to publish to Redis: {e}")
            return False

    async def consume(self, callback: Callable[[dict], Awaitable[None]]) -> None:
        logger.info(f"Starting Redis consumer on queue: {self.queue_name}")
        while True:
            try:
                # BLPOP returns a tuple (queue_name, element)
                result = await self.redis.blpop(self.queue_name, timeout=0)
                if result:
                    _, message_data = result
                    message = json.loads(message_data)
                    await callback(message)
            except Exception as e:
                logger.error(f"Error consuming from Redis: {e}")
                await asyncio.sleep(1) # Prevent tight loop on error
