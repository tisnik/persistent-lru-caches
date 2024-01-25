"""Cache that uses Memcache to store cached values."""

import threading
from typing import Union

from pymemcache.client.base import Client


class MemcacheCache():
    """Cache that uses Memcache to store cached values."""

    def __init__(self):
        """Create a new instance of the `MemcacheCache` class."""
        self.client = Client("localhost")

    def get(self, key: str) -> Union[str, None]:
        """Get the value associated with the given key.

        Args:
            key: The key for the desired value.

        Returns:
            The value associated with the key, or None if not found.
        """
        value = self.client.get(key)
        if value is None:
            return None
        return str(value)

    def insert_or_append(self, key: str, value: str) -> None:
        """Set the value associated with the given key.

        Args:
            key: The key for the value.
            value: The value to set.
        """
        oldValue = self.get(key)
        if oldValue:
            self.client.set(key, oldValue + "\n" + value)
        else:
            self.client.set(key, value)
