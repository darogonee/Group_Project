# NOTE Big help from charliegregg
from datetime import datetime, timedelta
import time

def cache(max_age=60):
    """
    A decorator to cache the result of a function call for a given time.
    :param max_age: the maximum time to cache the result in seconds
    """
    # create a decorator
    def decorator(function):
        # create a wrapper to run the function or return cached result
        class AgeCacheWrapper:
            cache = {}
            @staticmethod
            def clear(*args, **kwargs):
                # clear the cache for the given arguments
                AgeCacheWrapper.cache.pop(repr((args, tuple(kwargs.items()))))
                print(repr((args, tuple(kwargs.items()))))
            @staticmethod
            def clear_args(*args):
                # clear the cache for the given arguments and no restrictions on keywords
                matched = []
                for cache_key in AgeCacheWrapper.cache:
                    if cache_key.startswith(f"({repr((args))}"):
                        matched.append(cache_key)
                for match in matched:
                    AgeCacheWrapper.cache.pop(match)
            @staticmethod
            def __call__(*args, **kwargs):
                # find the cache key
                cache_key = repr((args, tuple(kwargs.items())))
                # check if the cache key is in the cache
                if cache_key in AgeCacheWrapper.cache:
                    result, timestamp = AgeCacheWrapper.cache[cache_key]
                    # if not expired, return the cached result
                    if datetime.now() < timestamp + timedelta(seconds=max_age):
                        return result
                # run the function and cache the result
                result = function(*args, **kwargs)
                # store the result with the timestamp
                AgeCacheWrapper.cache[cache_key] = (result, datetime.now())
                # return the result after caching
                return result
        # return the wrapper
        return AgeCacheWrapper()
    # return the decorator created
    return decorator

if __name__ == "__main__":
    @cache(max_age=10)
    def sleep(awake):
        time.sleep(1)
        return awake
    
    print(sleep(2))
    print(sleep(1))
    print(sleep(3))
    print(sleep(2))
    print(sleep(1))
    sleep.clear(1)
    print(sleep(1))
    print(sleep(3))
    print(sleep(2))