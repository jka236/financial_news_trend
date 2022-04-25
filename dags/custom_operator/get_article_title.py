from random_headers_list import headers_list
from soupify import soupify
from scrap_article_title import scrap_article_title

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

from redis_proxy_client import RedisProxyClient

from dag_config import Config as config
from random_headers_list import headers_list

class GetArticleTitleOperator(BaseOperator):
    
    @apply_defaults
    def __init__(
            self,
            # list_URL,
            redis_config, 
            redis_key,
            headers_list,
            *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.list_URL = list_URL
        self.redis_config = redis_config
        self.redis_key = redis_key
        self.headers_list = headers_list

    def execute(self, context):
        with RedisProxyClient(redis_config=config.REDIS_CONFIG, key='ips') as client:
            rss_feed_list = "Article scrap start"
            while rss_feed_list is not None:
                rss_feed_list = client.get_item(key='rss_feed_list')
                scrap_article_title(self.headers_list, self.redis_config, self.redis_key)
