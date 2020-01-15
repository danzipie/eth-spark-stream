# Apache Spark streaming of Ethereum transactions

The project implements this data flow:

blockchain source(*) ---> Apache Kafka producer --> Apache Spark stream

(*) provided by a websocket connection to Infura API.

It is a local development and needs to be modified for real scaling application.

## Quickstart

- Setup the Apache Kafka server (https://kafka.apache.org/quickstart)
- Setup Apache Spark
- `pip install -r requirements.txt`
- Start a new topic named 'chain':
```kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic chain```
- Start the producer:
```python3 transaction_feeder "wss://mainnet.infura.io/ws/v3/<YOUR_APP>"```
- Start the pyspark application:
```spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.4 transaction_streamer.py localhost:2181 chain```

## Troubleshoot
Starting the Apache Kafka server: first we need to start Zookeper, something like this:
`zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties & kafka-server-start /usr/local/etc/kafka/server.properties`