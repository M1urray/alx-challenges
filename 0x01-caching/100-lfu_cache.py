#!/usr/bin/python3
"""Least Frequently Used caching module.
"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """Represents an object that allows storing and
    retrieving items from a dictionary with a LFU
    removal mechanism when the limit is reached.
    """

    def __init__(self):
        """Initializes the cache instance.
        """
        super().__init__()
        self.keys = []
        self.uses = {}

    def put(self, key, item):
        """Adds an item in the cache.
        """
        if key is not None and item is not None:
            if (len(self.keys) == BaseCaching.MAX_ITEMS and
                    key not in self.keys):
                discard = self.keys.pop(self.keys.index(self.findLFU()))
                del self.cache_data[discard]
                del self.uses[discard]
                print('DISCARD: {:s}'.format(discard))
            self.cache_data[key] = item
            if key not in self.keys:
                self.keys.append(key)
                self.uses[key] = 0
            else:
                self.keys.append(self.keys.pop(self.keys.index(key)))
                self.uses[key] += 1

    def get(self, key):
        ''' Return value stored in `key` key of cache.
            If key is None or does not exist in cache, return None. '''
        if key is not None and key in self.cache_data:
            self.keys.append(self.keys.pop(self.keys.index(key)))
            self.uses[key] += 1
            return self.cache_data[key]
        return None

    def findLFU(self):
        ''' Return key of least frequently used item in cache.
            If multiple items have the same amount of uses, return the least
            recently used one. '''
        items = list(self.uses.items())
        freqs = [item[1] for item in items]
        least = min(freqs)

        lfus = [item[0] for item in items if item[1] == least]
        for key in self.keys:
            if key in lfus:
                return key
