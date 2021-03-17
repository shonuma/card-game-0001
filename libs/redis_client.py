import redis
import os
import json

client = redis.Redis(
    host=os.environ.get('REDIS_HOST') or 'localhost',
    port=os.environ.get('REDIS_PORT') or 6379,
)

class RedisClient:

    def __init__(self, namespace, host=None, port=None):
        if host and port:
            self._client = redis.Redis(
                host=host,
                port=port,
            )
        else:
            self._client = client
        self._namespace = namespace

    def _get_named_key(self, key):
        return '{}::{}'.format(
            self._namespace,
            key,
        )
    
    def _strip_namespace(self, named_key):
        return ''.join(named_key.split('::')[1:])

    def get(self, key):
        value = self._client.get(self._get_named_key(key))
        if isinstance(value, bytes):
            return value.decode()
        return value

    def get_multi(self, keys):
        """
        keysに与えられたキーを持つ辞書が返る
        """
        result = {}
        for key in keys:
            named_key = self._get_named_key(key)
            value = self._client.get(named_key)
            if value:
                value = value.decode()
            result[self._strip_namespace(named_key)] = value
        return result

    def set(self, key, value, timeout=60):
        self._client.set(
            self._get_named_key(key),
            value,
            ex=timeout,
        )

    def set_multi(self, dict_, timeout=60):
        for key, value in dict_.items():
            converted_key = self._get_named_key(key)
            self._client.set(converted_key, value, ex=timeout)

    def get_keys_by_prefix(self, prefix):
        result = []
        query = '{}*'.format(self._get_named_key(prefix))
        for key in self._client.scan_iter(query):
            result.append(
                self._strip_namespace(key.decode())
            )
        return result

    def delete(self, keys):
        for key in keys:
            self._client.delete(
                self._get_named_key(key)
            )
