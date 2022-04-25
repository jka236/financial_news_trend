from bs4 import BeautifulSoup
import requests
import random
import re

def soupify(web_url:str, headers_list:list, parser : str, proxy: str=None) -> BeautifulSoup: 
    header = random.choice(headers_list)
    try:
        if proxy is None:
            req = requests.get(web_url , headers=header, timeout=5)
        else:
            protocol = re.match('^https?',proxy).group()
            proxy = {protocol:proxy}
            req = requests.get(web_url , headers=header, proxies=proxy, timeout=5)
        soup = BeautifulSoup(req.text, parser)
        return soup
    except Exception as err:
        raise Exception(err)
