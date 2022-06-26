from redis_proxy_client import RedisProxyClient


from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

class ProxyPoolOperator(BaseOperator):

    @apply_defaults
    def __init__(
            self,
            proxy_list_URL,
            redis_config,
            redis_key,
            headers_list,
            *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxy_list_URL = proxy_list_URL
        self.redis_config = redis_config
        self.redis_key = redis_key
        self.headers_list = headers_list
        
    def execute(self, context):
        with RedisProxyClient(self.redis_config, self.redis_key) as client:
            client.scrap_proxy(self.proxy_list_URL, self.headers_list)