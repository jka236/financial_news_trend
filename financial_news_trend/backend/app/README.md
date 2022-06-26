# Buzz Finder

This is a data engineering full stack project that consumes the daily news RSS and shows the top 5 most frequent keywords. 

<img width="1256" alt="image" src="https://user-images.githubusercontent.com/83562725/173284799-1b42a794-c50b-4277-8a13-6210cd2397d2.png">

## How it works
**Data Scraping**

Airflow DAG is responsible for the execution of Python scraping modules. It runs once a day producing a batch of word counting.

The first task creates a list of proxies. With the proxy list in combination with rotating user agents, it helps the scraper pass the anti-scraping measures

The second task extracts RSS feed list and stores them in Redis. 

In the last task scrap article titles from the RSS list generated from the second task. Article titles are passed to Kafka topic "article_title" and it is consumed by Apache Beam 

**Data Process**

Apache Beam is in charge of the data process. Ingested article titles are split into a single word and counted in the number of occurrences. Input to Apache Beam is consuming streaming data ingestion whereas it returns a batch of word counting. The window of the streaming is ten minutes which is enough to ingest all daily article titles from Airflow. Apache Beam could be a part of the Airflow task, but it is not included due to the lack of computing power. 

**Data Visualization**

Processed data is stored in MongoDB. FastAPi+Next.js stack is fetching data from MongoDB and visualizing with D3.js

