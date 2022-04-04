import json
import redis

class RedisProxyClient:
    def __init__(self, key, redis_config):
        self.key = key
        self.redis = redis.Redis(
            **redis_config
        )

    def __enter__(self):
        return self

    def list_existing_proxies(self):
        response = self.redis.lrange(self.key, 0, -1)
        return [
            json.loads(proxy) for proxy in response
        ]
    
    def push_proxy(self, value):
        redis.lpush(self.key, value)

    def get_proxy(self):
        existing_proxies = self.list_existing_proxies()
        if len(existing_proxies) > 0:
            return existing_proxies[0]

    def lpop_proxy(self):
        self.redis.lpop(self.key)

    def __exit__(self, type, value, traceback):
        client_id = self.redis.client_id()
        self.redis.client_kill_filter(
            _id=client_id
        )
