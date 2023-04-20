#!/usr/bin/python3
''' First-In First-Out caching module. '''

BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    ''' Represents an object that allows storing and
    retrieving items from a dictionary with a FIFO
    removal mechanism when  limit is reached.
    '''

    def __init__(self):
        """Initializes the cache.
        """
        super().__init__()
        self.key_indexes = []

    def put(self, key, item):
        """Adds an item to the cache.
        """
        if key and item:
            if key in self.cache_data:
                self.cache_data[key] = item
                return

            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discarded_item = self.key_indexes.pop(0)
                del self.cache_data[discarded_item]
                print("DISCARD:", discarded_item)

            self.cache_data[key] = item
            self.key_indexes.append(key)

    def get(self, key):
        """Retrieves an item by key.
        """
        if key in self.cache_data:
            return self.cache_data[key]
        return None
