import redis_proxy_client
from bs4 import BeautifulSoup
import redis
from urllib.request import Request, urlopen
from random_headers_list import headers_list
import random

def scrap_proxy(proxy_list_URL:str, headers_list:list):
    # Get proxies from free proxy website 
    client = redis.Redis(host='localhost', port=6379, db=0)
    client.flushdb()
    # URL = "https://free-proxy-list.net/"
    soup = soupify(proxy_list_URL, headers_list, "html.parser")
    table = soup.find("table", class_="table table-striped table-bordered")
    table_body = table.find("tbody")
    proxy_element = table_body.find_all("tr")
    
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
        client.lpush(tr_idx, proxy)

def scrap_title(rss_feed_URL:str, headers_list:list) -> list:
    soup = soupify(rss_feed_URL, headers_list, "html.parser")
    titles = soup.find_all('title')
    title_list = [title.text for title in titles]
    return title_list

def scrap_rss_feed_list(list_URL:str, headers_list:list) -> list:
    soup = soupify(list_URL, headers_list, "html.parser")
    rss_feeds = soup.find_all('a','ext')
    return [rss_feed['href'] for rss_feed in rss_feeds]

def soupify(web_url:str, headers_list:list, parser:str) -> BeautifulSoup: 
    header = random.choice(headers_list)
    req = Request(web_url , headers=header)
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, parser)
    return soup

# connect to redis
if __name__ == "__main__":
    rss_list = scrap_rss_feed_list("https://blog.feedspot.com/business_news_rss_feeds", headers_list)
    # print(rss_list)
    print(scrap_title(rss_list[0]))   
 
 
