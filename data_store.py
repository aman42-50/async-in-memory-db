import time
import math
from typing import Dict


class Entry:
    def __init__(self, value: str):
        self.value = value
        self.expires_at = None

    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at


class DataStore:
    def __init__(self):
        self._store: Dict[str, Entry] = {}

    def set(self, key, value):
        self._store[key] = Entry(value)

    def get(self, key):
        if key not in self._store:
            return None

        entry = self._store[key]

        if entry.is_expired():
            del self._store[key]
            return None

        return entry.value

    def delete(self, key) -> bool:
        value = self.get(key)
        if value is None:
            return False
        del self._store[key]
        return True

    def expire(self, key, seconds):
        value = self.get(key)
        if value is None:
            return False

        entry = self._store[key]
        entry.expires_at = time.time() + seconds

        return True

    def get_ttl(self, key) -> int:
        value = self.get(key)
        if value is None:
            return -2

        entry = self._store[key]

        if entry.expires_at is None:
            return -1

        return int(math.ceil(entry.expires_at - time.time()))
