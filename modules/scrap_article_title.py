from soupify import soupify
from redis_proxy_client import RedisProxyClient
from random_headers_list import headers_list
from json import dumps
from kafka import KafkaProducer

def scrap_article_title(headers_list, redis_config, redis_key):
    redis = RedisProxyClient(redis_config, redis_key)
    rss_feed_URL = redis.lpop_item('rss_feed_list')
    redis.health_check()
    producer = KafkaProducer(bootstrap_servers='kafka:9092')

    try:
        proxy = redis.get_item()
        soup = soupify(rss_feed_URL, headers_list, "html.parser", proxy)
        titles = soup.find_all('title')
        title_list = list(set([title.text for title in titles]))
        for title in title_list:
            if redis.sadd_item(key='article_title', value=title) == 1:
                print(title)
                producer.send('article_title', str.encode(title))
                producer.flush()
    except Exception as err:
        print(err)
            
def get_text(soup_with_tag):
    return soup_with_tag.text

if __name__ == "__main__":
    REDIS_CONFIG = {
        "host": "localhost",
        "port": "6378",
        "db": 0
    }
    scrap_article_title(
                        redis_config=REDIS_CONFIG,
                        redis_key='ips',
                        headers_list=headers_list
                        )