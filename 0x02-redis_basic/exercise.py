#!/usr/bin/env python3
"""
Writing strings to Redis
Reading from Redis and recovering original type
Incrementing values
Storing lists
Retrieving lists
"""

import redis
import uuid
from typing import Union, Callable, Optional, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
     Count how many times methods of the Cache class are called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Store the history of inputs and outputs for a particular function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        result = method(self, *args)
        # adding the result to the list
        self._redis.rpush(f"{method.__qualname__}:outputs", result)
        return result
    return wrapper


def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function.
    """
    # access redis instance stored in method's object
    redis_instance = method.__self__._redis

    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"
    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)
    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for input_data, output_data in zip(inputs, outputs):
        print(f"{method.__qualname__}(*({input_data.decode()})) -> "
              f"{output_data.decode()}")


class Cache:
    """Contains __init__ and store methods"""

    def __init__(self) -> None:
        """
        Stores an instance of the Redis client as _redis using redis.Redis()
        Flushes the instances using flushdb
        """
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Takes a data arg and returns a string
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
        Take a key string argument and an optional Callable argument
        named fn
        This callable will be used to convert the data
        back to the desired format.
        """
        if not self._redis.exists(key):
            return None
        if fn is not None:
            data = self._redis.get(key)
            return fn(data)
        else:
            return self._redis.get(key)

    def get_str(self, key: str) -> str:
        """Converts bytes to str"""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Converts bytes to int"""
        return self.get(key, lambda x: int(x))
