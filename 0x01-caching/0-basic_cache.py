#!/usr/bin/python3
''' Basic caching module. '''

BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    ''' Represents an object that allows storing and
    retrieving items from a dictionary.'''

    def put(self, key, item):
        ''' Adds an item in the cache. '''
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        ''' Retrieves an item by key. '''
        if key in self.cache_data:
            return self.cache_data[key]
        return None
