from time import sleep
from json import dumps
from kafka import KafkaProducer

if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    print('producer?')
    some_string = 'string'
    producer.send('article_title', str.encode(some_string))
    producer.flush()
    print('done')