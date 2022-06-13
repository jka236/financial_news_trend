# Buzz Finder

This is a data engineering full stack project that consumes the daily news RSS and shows the top 5 most frequent keywords. 

<img width="1256" alt="image" src="https://user-images.githubusercontent.com/83562725/173284799-1b42a794-c50b-4277-8a13-6210cd2397d2.png">

## How it works
**Data Scraping**
Airflow DAG is responsible for the execution of Python scraping modules. It runs periodically every X minutes producing micro-batches.

First task updates proxypool. Using proxies in combination with rotating user agents can help get scrapers past most of the anti-scraping measures and prevent being detected as a scraper.

Second task extracts news from RSS feeds provided in the configuration file, validates the quality and sends data into Kafka topic A. The extraction process is using validated proxies from proxypool.

**Data flow**
Kafka Connect Mongo Sink consumes data from Kafka topic A and stores news in MongoDB using upsert functionality based on _id field.
Debezium MongoDB Source tracks a MongoDB replica set for document changes in databases and collections, recording those changes as events in Kafka topic B.
Kafka Connect Elasticsearch Sink consumes data from Kafka topic B and upserts news in Elasticsearch. Data replicated between topics A and B ensures MongoDB and ElasticSearch synchronization. Command Query Responsibility Segregation (CQRS) pattern allows the use of separate models for updating and reading information.
Kafka Connect S3-Minio Sink consumes records from Kafka topic B and stores them in MinIO (high-performance object storage) to ensure data persistency.

**Data access**
Data gathered by previous steps can be easily accessed in API service using public endpoints.
