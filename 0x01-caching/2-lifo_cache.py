#!/usr/bin/python3
"""Last-In First-Out caching module.
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """Represents an object that allows storing and
    retrieving items from a dictionary with a LIFO
    removal mechanism when the limit is reached.
    """

    def __init__(self):
        """Initializes the cache.
        """
        super().__init__()
        self.key_indexes = []

    def put(self, key, item):
        """Adds an item in the cache.
        """
        if key and item:
            if len(self.cache_data) >= self.MAX_ITEMS:
                if key in self.cache_data:
                    del self.cache_data[key]
                    self.key_indexes.remove(key)
                else:
                    del self.cache_data[self.key_indexes[self.MAX_ITEMS - 1]]
                    item_discarded = self.key_indexes.pop(self.MAX_ITEMS - 1)
                    print("DISCARD:", item_discarded)

            self.cache_data[key] = item
            self.key_indexes.append(key)

    def get(self, key):
        """Retrieves an item by key.
        """
        if key in self.cache_data:
            return self.cache_data[key]
        return None
