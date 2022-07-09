#!/bin/bash
pwd
docker-compose -f docker-compose.yml up -d

sleep 1m

cd /Users/jonghyeokkim/Desktop/Coding/financial_news_trend/scrap/word-count-beam

mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.MinimalWordCount

sleep 15m
cd /Users/jonghyeokkim/Desktop/Coding/financial_news_trend
docker-compose down