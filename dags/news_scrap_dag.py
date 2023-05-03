from datetime import datetime, timedelta
from textwrap import dedent
from custom_operator.get_rss_list import GetRSSListOperator
from custom_operator.get_proxy_list import ProxyPoolOperator
from custom_operator.get_article_title import GetArticleTitleOperator
from dag_config import Config as config
from random_headers_list import headers_list


# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
# from airflow.operators.bash import BashOperator

def event_export(id, redis_config, redis_key, headers_list, idx):
    return GetArticleTitleOperator(
                                    task_id=f'getArticleTitles{id}',
                                    redis_config=redis_config,
                                    redis_key=redis_key,
                                    headers_list=headers_list, 
                                    idx=idx                                  
                                    )

def create_dag(dag_id, rss_news, schedule_interval,idx):
    with DAG(
        # These args will get passed on to each operator
        # You can override them on a per-task basis during operator initialization
        default_args={
            'depends_on_past': False,
            'email': ['jk23oct@gmail.com'],
            'email_on_failure': True,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=5),
        },
        dag_id=dag_id,
        description=f'A DAG for {rss_news}',
        schedule_interval=schedule_interval,
        start_date=datetime(2022, 4, 23),
        catchup=False,
        is_paused_upon_creation=False,
    ) as dag:

        get_proxy_list = ProxyPoolOperator(
                                        task_id='getProxyList',
                                        proxy_list_URL="https://free-proxy-list.net",
                                        redis_config=config.REDIS_CONFIG,
                                        redis_key='ips',
                                        headers_list=headers_list
                                        )
        
        get_rss_list = GetRSSListOperator(
                                        task_id='getRSSList',
                                        list_URL=rss_feeds, 
                                        redis_config=config.REDIS_CONFIG,
                                        redis_key='ips',
                                        headers_list=headers_list, 
                                        idx=idx
                                        )
        
        get_article_titles = GetArticleTitleOperator(
                                        task_id='getArticleTitles',
                                        redis_config=config.REDIS_CONFIG,
                                        redis_key='ips',
                                        headers_list=headers_list,      
                                        idx=idx                             
                                        )
        
        get_proxy_list >> get_rss_list >> get_article_titles 
        
    return dag

for n, rss_feeds in enumerate(config.RSS_FEED_LIST):
    dag_id = f"rss_news_{n}"
    schedule_interval = "0 * * * *"

    globals()[dag_id] = create_dag(
        dag_id,
        rss_feeds,
        schedule_interval,
        n
    )