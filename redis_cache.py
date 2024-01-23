"""Cache that uses Redis to store cached values."""

import threading
from typing import Union

import redis


class RedisCache():
    """Cache that uses Redis to store cached values."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, max_memory="100mb"):
        """Create a new instance of the `RedisCache` class."""
        with cls._lock:
            if not cls._instance:
                cls._instance = super(RedisCache, cls).__new__(cls)
                cls._instance.initialize_redis(max_memory)
        return cls._instance

    def initialize_redis(self, max_memory) -> None:
        """Initialize the Redis client and logger.

        This method sets up the Redis client with custom configuration parameters.
        """
        self.redis_client = redis.StrictRedis(
            host="localhost",
            port="6379",
            decode_responses=True,
        )
        # Set custom configuration parameters
        self.redis_client.config_set("maxmemory", max_memory)
        self.redis_client.config_set("maxmemory-policy", "allkeys-lru")
        self.redis_client.config_set("maxmemory-samples", "10")
        #self.redis_client.config_set("maxmemory-policy", "allkeys-lfu")
        #self.redis_client.config_set("maxmemory-policy", "noeviction")

    def get(self, key: str) -> Union[str, None]:
        """Get the value associated with the given key.

        Args:
            key: The key for the desired value.

        Returns:
            The value associated with the key, or None if not found.
        """
        return self.redis_client.get(key) or ""

    def insert_or_append(self, key: str, value: str) -> None:
        """Set the value associated with the given key.

        Args:
            key: The key for the value.
            value: The value to set.
        """
        oldValue = self.get(key)
        with self._lock:
            if oldValue:
                self.redis_client.set(key, oldValue + "\n" + value)
            else:
                self.redis_client.set(key, value)
