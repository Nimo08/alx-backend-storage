#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""

import redis
import requests
from typing import Callable, Any
from functools import wraps


def get_page(url: str) -> str:
    """
    Uses the requests module to obtain the HTML content
    of a particular URL and returns it.
    """
    redis_instance = redis.Redis()
    count_key = f"count:{url}"
    redis_instance.incr(count_key)
    cached_response = redis_instance.get(url)
    if cached_response:
        return cached_response.decode()
    response = requests.get(url)
    html_content = response.text
    redis_instance.setex(url, 10, html_content)
    return html_content


if __name__ == "__main__":
    print(get_page('http://slowwly.robertomurray.co.uk'))
