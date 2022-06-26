import redis
from soupify import soupify
import requests
from soupify import soupify
from random_headers_list import headers_list

class RedisProxyClient:
    def __init__(self, redis_config, key):
        self.key = key
        self.redis = redis.Redis(
            **redis_config
        )

    def __enter__(self):
        return self

    def list_existing_items(self, key=None):
        if key == None:
            key = self.key
        return self.redis.lrange(key, 1, -1)
    
    def scrap_proxy(self, proxy_list_URL: str, headers_list: list):
        # URL = "https://free-proxy-list.net/"
        soup = soupify(proxy_list_URL, headers_list, "html.parser")
        table = soup.find("table", class_="table table-striped table-bordered")
        table_body = table.find("tbody")
        proxy_element = table_body.find_all("tr")
        
        proxy_list = []
        for tr_idx, elem in enumerate(proxy_element):
            for idx, td in enumerate(elem):
                if(idx == 0):
                    ip = str(td.text)
                if(idx == 1):
                    port = str(td.text)
                if(idx == 6):
                    https = str(td.text)
            if https == 'yes': 
                proxy = f'https://{ip}:{port}'
            else:
                proxy = f'http://{ip}:{port}'
            proxy_list.append(proxy)
            
        self.redis.lpush(self.key, *proxy_list)
    
    def override_existing_proxies(self, proxies, key=None):
        if key == None:
            key = self.key
        self.logger.info(f"Overriding existing proxies {proxies}")
        self.redis.delete(key)
        self.redis.lpush(key, *proxies)

    def insert_item(self, value, key=None):
        if key == None:
            key = self.key
        self.redis.lpush(key, value)
        
    def insert_item_list(self, *value, key=None):
        if key == None:
            key = self.key
        return self.redis.lpush(key, *value)
    
    def sadd_item(self, value, key=None):
        if key == None:
            key = self.key
        return self.redis.sadd(key, value)
    
    def sadd_item_list(self, *value, key=None):
        if key == None:
            key = self.key
        self.redis.sadd(key, *value)
        
    def another_sadd(self, *value, key):
        self.redis.sadd(key, *value)
        
    def get_item(self, key=None):
        if key == None:
            key = self.key
        existing_proxies = self.list_existing_items(key)
        if len(existing_proxies) > 0:
            return existing_proxies[0]

    def lpop_item(self, key=None):
        if key == None:
            key = self.key
        return self.redis.lpop(key)
    
    def health_check(self):
        success = False
        while success is False and self.get_item() is not None:
            try:
                proxy = self.get_item()
                soup = soupify("https://google.com", headers_list, "html.parser", proxy)
                success = True
            except Exception as err:
                self.lpop_item()
    
    def __exit__(self, type, value, traceback):
        client_id = self.redis.client_id()
        self.redis.client_kill_filter(
            _id=client_id
        )
