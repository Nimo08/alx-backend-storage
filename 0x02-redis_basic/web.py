#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""

import redis
import requests
from typing import Callable
from functools import wraps


def count_url(func: Callable) -> Callable:
    """
    Track how many times a particular URL was accessed
    in the key "count:{url}" and cache the result with an
    expiration time of 10 seconds
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        redis_instance = redis.Redis()
        redis_instance.incr(f"count:{url}")
        cached_response = redis_instance.get(f"{url}")
        if cached_response:
            return cached_response.decode('utf-8')
        result = func(url)
        redis_instance.setex(f"result:{url}", 10, result)
        return result
    return wrapper


@count_url
def get_page(url: str) -> str:
    """
    Uses the requests module to obtain the HTML content
    of a particular URL and returns it.
    """
    response = requests.get(url)
    return response.text
