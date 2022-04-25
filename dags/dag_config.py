class Config:
    RSS_FEED_LIST=[ 
                    "https://blog.feedspot.com/business_news_rss_feeds/", 
                    "https://blog.feedspot.com/business_magazines/",
                    "https://blog.feedspot.com/canadian_news_rss_feeds/",
                    "https://blog.feedspot.com/world_news_rss_feeds/",
                    "https://blog.feedspot.com/usa_news_rss_feeds/"
                  ]
    REDIS_CONFIG = {
        "host": "proxy-redis",
        "port": "6379",
        "db": 0
    }
