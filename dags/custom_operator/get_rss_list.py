from random_headers_list import headers_list
from soupify import soupify
from scrap_rss_feed_list import scrap_rss_feed_list

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults


class GetRSSListOperator(BaseOperator):

    @apply_defaults
    def __init__(
            self,
            list_URL,
            redis_config, 
            redis_key,
            headers_list,
            *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_URL = list_URL
        self.redis_config = redis_config
        self.redis_key = redis_key
        self.headers_list = headers_list

    def execute(self, context):
        scrap_rss_feed_list(self.list_URL, self.headers_list, self.redis_config, self.redis_key)