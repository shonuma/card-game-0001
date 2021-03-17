from libs.redis_client import RedisClient
import os
import unittest

client = RedisClient('test', host='localhost', port=6379)


def populate():
    keys = client.get_keys_by_prefix('key')
    client.delete(keys)
    client.set('key1', 'value1')
    client.set('key2', 3)
    client.set('key3', 'value2')
    client.set('key3', 4)

populate()

class TestRedisClient(unittest.TestCase):


    def test_get(self):
        self.assertEqual(client.get('key1'), 'value1')
        self.assertEqual(client.get('key2'), '3')
        self.assertEqual(client.get('key3'), '4')

    def test_get_keys_by_prefix(self):
        keys = sorted(client.get_keys_by_prefix('key'))
        self.assertEqual(
            keys,
            ['key1', 'key2', 'key3']
        )
    
    def test_get_multi(self):
        client.set_multi(
            {'key5': 6, 'key7': 8.9, 'key10': 'key11'}
        )
        keys = ['key5', 'key10', 'key12']
        r = client.get_multi(keys)
        self.assertEqual(r['key5'], '6')
        self.assertEqual(r['key10'], 'key11')
        self.assertEqual(r['key12'], None)

    


if __name__ == '__main__':
    unittest.main()
