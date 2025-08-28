"""Short-term memory cache module."""

class CatchMemory:
    def __init__(self):
        self.store = {}

    def remember(self, key: str, value):
        self.store[key] = value

    def recall(self, key: str):
        return self.store.get(key)
