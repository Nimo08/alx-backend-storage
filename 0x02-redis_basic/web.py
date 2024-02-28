#!/usr/bin/env python3
"""
"""

import redis
import requests
from typing import Callable, Any
from functools import wraps
redis_instance = redis.Redis()


def count(func: Callable) -> Callable:
    """
    Track how many times a particular URL was accessed
    in the key "count:{url}" and cache the result with an
    expiration time of 10 seconds
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> Any:
        url = args[0]
        count_key = f"count:{url}"
        redis_instance.incr(count_key)
        return func(self, *args, **kwargs)
    return wrapper


def get_page(url: str) -> str:
    """
    Uses the requests module to obtain the HTML content
    of a particular URL and returns it.
    """
    cached_response = redis_instance.get(url)
    if cached_response:
        return cached_response.decode('utf-8')
    response = requests.get(url)
    html_content = response.text

    redis_instance.setex(url, 10, html_content)
    return html_content


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    html_content = get_page(url)
    print(html_content)
