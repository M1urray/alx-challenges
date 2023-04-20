#!/usr/bin/python3
"""Most Recently Used caching module.
"""

from collections import OrderedDict

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """Represents an object that allows storing and
    retrieving items from a dictionary with an MRU
    removal mechanism when the limit is reached.
    """

    def __init__(self):
        """Initializes the cache.
        """
        super().__init__()
        self.mru_order = OrderedDict()

    def put(self, key, item):
        """Adds an item in the cache.
        """
        if not key or not item:
            return

        self.cache_data[key] = item
        self.mru_order[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            item_discarded = next(iter(self.mru_order))
            del self.cache_data[item_discarded]
            print("DISCARD:", item_discarded)

        if len(self.mru_order) > BaseCaching.MAX_ITEMS:
            self.mru_order.popitem(last=False)

        self.mru_order.move_to_end(key, False)

    def get(self, key):
        """Retrieves an item by key.
        """
        if key in self.cache_data:
            self.mru_order.move_to_end(key, False)
            return self.cache_data[key]
        return None
