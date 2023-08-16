#!/usr/bin/python3
"""exercise module."""
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


class Cache():
    """A Cache class that uses redis to store and retrieve data"""
    
    def __init__(self):
        """Init method that instanciates _redis"""
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @staticmethod
    def count_calls(method: Callable) -> Callable:
        """decorates a method to count how many times it was called"""

        @wraps(method)
        def wrapped(self, *args, **kwargs):
            """wrapper function"""
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapped

    @staticmethod
    def call_history(method: Callable) -> Callable:
        """decorates a method to record its input output history"""
        @wraps(method)
        def wrapped(self, *args, **kwargs):
            """wrapper method"""
            input_key = "{}:inputs".format(method.__qualname__)
            output_key = "{}:outputs".format(method.__qualname__)

            self._redis.rpush(input_key, str(args))
            result = method(self, *args, **kwargs)
            self._redis.rpush(output_key, result)

            return result
        return wrapped

    def replay(method: Callable):
        """
        displays the history of calls made by a particular method by retrieving
        the inputs and outputs saved on the redis store
        """
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)

        inputs = method._redis.lrange(input_key, 0, -1)
        outputs = method._redis.lrange(output_key, 0, -1)

        print(f"{method.__qualname__} was called {len(inputs)} times:")
        for args, output in zip(inputs, outputs):
            args_str = args.decode("utf-8")
            output_str = output.decode("utf-8")
            print(f"{method.__qualname__}(*{args_str}) -> {output_str}")

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Takes a data argument and returns a string"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable]\
        = None) -> Union[str, bytes, int, float, None]:
        """
        returns the data value stored in the redis store at the key
        by converting it to its original data type by calling the
        function fn. if the key is not found, it returns None
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        returns the value stored in the reds store at the key as str
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        returns the value stored in the redis store at the key as an int
        """
        return self.get(key, fn=int)
