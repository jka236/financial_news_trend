from bs4 import BeautifulSoup
import redis
from urllib.request import Request, urlopen
import requests
from random_headers_list import headers_list
import random
import re
import numpy as np
from custom_operator.get_proxy_list import ProxyPoolOperator
from redis_proxy_client import RedisProxyClient

from dag_config import Config as config
from random_headers_list import headers_list


def get_proxy(key):
    client = redis.Redis(host='localhost', port=6378, db=0, decode_responses=True)
    return client.lrange(key, 0, -1)

def scrap_proxy(proxy_list_URL: str, headers_list: list):
    # Get proxies from free proxy website 
    
    client = redis.Redis(host='localhost', port=6378, db=0)
    client.flushdb()
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

    client.lpush('proxy_list', *proxy_list)

def scrap_title(rss_feed_URL:str, headers_list:list, proxy: str="") -> list:
    soup = soupify(rss_feed_URL, headers_list, "html.parser", proxy)
    titles = soup.find_all('title')
    titles = np.array(titles)
    extract_text = np.vectorize(get_text)
    title_list = extract_text(titles)
    # title_list = [title.text for title in titles]
    return title_list

def get_text(soup_with_tag):
    return soup_with_tag.text

def scrap_rss_feed_list(list_URL:str, headers_list:list, proxy: str="") -> list:
    soup = soupify(list_URL, headers_list, "html.parser", proxy)
    rss_feeds = soup.find_all('a','ext')
    return [rss_feed['href'] for rss_feed in rss_feeds]

def soupify(web_url:str, headers_list:list, parser : str, proxy: str="") -> BeautifulSoup: 
    header = random.choice(headers_list)
    try:
        protocol = re.match('^https?',proxy).group()
        proxy = {protocol:proxy}
        req = requests.get(web_url , headers=header, proxies=proxy)
    except:
        req = requests.get(web_url , headers=header)
    # webpage = urlopen(req).read()
    soup = BeautifulSoup(req.text, parser)
    return soup

# connect to redis
if __name__ == "__main__":
    client = RedisProxyClient(            
            redis_config=config.REDIS_CONFIG,
            key='ips',
            )
    client.scrap_proxy("https://free-proxy-list.net", headers_list)
    proxy = client.get_proxy()
    print(proxy)
    # rss_list = scrap_rss_feed_list("https://blog.feedspot.com/business_news_rss_feeds", headers_list, proxy)
    # print(scrap_title(rss_list[0], headers_list, proxy))
    
    # for rss in rss_list[:1]:
        # print(scrap_title(rss, headers_list, proxy))
    # print(proxy)

 
 
