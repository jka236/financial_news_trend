#!/bin/sh

curl -X POST \
     -H "Content-Type: application/json" \
     --data '
     {"name": "mongo-sink",
      "config": {
         "connector.class":"com.mongodb.kafka.connect.MongoSinkConnector",
         "connection.uri":"mongodb+srv://rss_feed:rss_feed@cluster0.46sfz.mongodb.net/?retryWrites=true&w=majority",
         "tasks.max": "1",
         "database":"rss_feed",
         "collection":"rss_feed",
         "topics":"new_topic3",
         "key.converter": "org.apache.kafka.connect.json.JsonConverter",
         "key.converter.schemas.enable": false,
         "value.converter": "org.apache.kafka.connect.json.JsonConverter",
         "value.converter.schemas.enable": false
         }
     }
     ' \
     http://connector:8083/connectors -w "\n"


curl -X PUT http://connector:8083/connectors/mongo-sink/config -H "Content-Type: application/json" -d \
'
      {
         "connector.class":"com.mongodb.kafka.connect.MongoSinkConnector",
         "connection.uri":"mongodb+srv://rss_feed:rss_feed@cluster0.46sfz.mongodb.net/?retryWrites=true&w=majority",
         "tasks.max": "1",
         "database":"rss_feed",
         "collection":"rss_feed",
         "topics":"rss_feed",
         "key.converter": "org.apache.kafka.connect.json.JsonConverter",
         "key.converter.schemas.enable": false,
         "value.converter": "org.apache.kafka.connect.json.JsonConverter",
         "value.converter.schemas.enable": false
         }
     '

curl -X DELETE http://connector:8083/connectors/mongo-sink