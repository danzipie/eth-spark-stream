import sys

from pyspark.streaming.kafka import KafkaUtils
from pyspark.streaming import StreamingContext
from pyspark import SparkContext

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: transaction_streamer.py <zk> <topic>", file=sys.stderr)
        exit(-1)

    sc = SparkContext(appName="TransactionStreamer")
    sc.setLogLevel("ERROR")
    avg_block_time = 15
    ssc = StreamingContext(sc, batchDuration=avg_block_time)

    zkQuorum, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    kvs.pprint()
    
    ssc.start()
    ssc.awaitTermination()
