## news-streams project

[![Build Status](https://jenkins-proxy.spookyai.com/job/news-streams/job/main/badge/icon)](http://jenkins.ww.home:8080/job/news-streams/job/main/)

## news_stream_django
1. Required environment variables
    - MONGODB_URI
      - A Mongodb Uri with username, password and mongodb dns
    - MEMCACHED_SERVICE
      - A Memcached service DNS name which include all Memcached IP addresses
      - Client can resolve this DNS name to get all IPs in this Memcached cluster
    - ELASTIC_HOST
      - An Elasticsearch local host to get search results in Elasticsearch database
2. How to run after setting environment variables
    - direct to news_stream_django folder 
      - run command
      '''
      python manage.py
      '''
3. Endpoints
    - /api 
      - to get all twitters information according to SocialPost model including required hashtags
      - Return format: Json
    - /api/trending 
      - to get all recently mentioned top counted hashtags aggregate from mongodb
      - Return format: Json
    - /api/tags/{tag} 
      - to get tweets which text including specified tag  
      - param need to pass: string of tag pass from frontend url
      - Return format: Json
    - /health 
      - to check whether app is health
    - /metrics 
      - to get kafka received tweets and processed tweets
    
## news_stream_frontend
   - React command to run on Android 


## news_stream_streams
1. Required environment variables
   - CONSUMER_KEY / CONSUMER_SECRET / ACCESS_TOKEN / ACCESS_TOKEN_SECRET /BEARER_TOKEN
      - twitterAPI credentials
   - KAFKA_BOOTSTRAP_SERVERS
      - a list of host/post pairs separated by "," to establish initial connection to the Kafka cluster
   - KAFKA_GROUP_CONSUMER
      - a Kafka consumer name which cooperate multiple consumers to consume data from same topics
   - MONGODB_URI
     - A Mongodb Uri with username, password and mongodb dns
   - ELASTIC_HOST
      - An Elasticsearch local host to get search results in Elasticsearch database
2. How to run after setting environment variables
   - direct to news_stream_stream folder
     - run command to get Twitter stream and produce raw data to Kafka
       ```
       python twitter_stream.py
       ```
     - run command to start consume and process data and insert into database
       ```
       python kafka_main.py
       ```
3. streams (from twitter and reddit)
    - filtered twitter posts according to twitterAPI rule
    - add kafka producer to the filtered tweets and prometheus metrics
    - add kafka consumer and prometheus metrics before insert data into mongodb database
4. models
   - SocialPost model to parse required fields from twitter posts with related tags
5. mongo_query
   - mongo aggregation to have top counted hashtags and converted to python based
   - merge same categories of hashtags into one list and sum counts
   - add to memcache to reduce database queries times


## Dockerfiles
Dockerfile for both streams and django service which can be built in CI to docker image

## Deploy
Contains Kubernetes configurations for all components which includes:
    - backend-api
    - memcached
    - news-streams
    