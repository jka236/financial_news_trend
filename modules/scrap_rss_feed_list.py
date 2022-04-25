from soupify import soupify
from redis_proxy_client import RedisProxyClient
from random_headers_list import headers_list

def scrap_rss_feed_list(list_URL, headers_list, redis_config, redis_key):
    redis = RedisProxyClient(redis_config, redis_key)
    redis.health_check()

    try:
        proxy = redis.get_item()
        soup = soupify(list_URL, headers_list, "html.parser", proxy)
        rss_feeds = soup.find_all('a','ext')
        rss_feed_list = [rss_feed['href'] for rss_feed in rss_feeds]
        redis.insert_item_list(*rss_feed_list, key='rss_feed_list')
    except Exception as err:
        print(err)
        redis.lpop_item()
            
if __name__ == "__main__":
    REDIS_CONFIG = {
        "host": "localhost",
        "port": "6378",
        "db": 0
    }
    scrap_rss_feed_list(list_URL="https://blog.feedspot.com/business_news_rss_feeds", 
                                    redis_config=REDIS_CONFIG,
                                    redis_key='ips',
                                    headers_list=headers_list)