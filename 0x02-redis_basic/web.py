#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""

import redis
import requests
from typing import Callable, Any
from functools import wraps
redis_instance = redis.Redis()


def count_url(func: Callable) -> Callable:
    """
    Track how many times a particular URL was accessed
    in the key "count:{url}" and cache the result with an
    expiration time of 10 seconds
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        redis_instance.incr(count_key)
        cached_response = redis_instance.get(url)
        if cached_response:
            return cached_response.decode('utf-8')
        html_content = func(url)
        redis_instance.setex(url, 10, html_content)
        return html_content
    return wrapper


@count_url
def get_page(url: str) -> str:
    """
    Uses the requests module to obtain the HTML content
    of a particular URL and returns it.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
