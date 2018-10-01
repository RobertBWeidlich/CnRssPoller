file:    Readme-kafka.md
author:  rbw
date:    Mon Oct  1 13:41:59 PDT 2018
purpose: Addition of Kafka to CnRssPoller

Rough notes...

0. Download and install Kafka

1. Download and install Zookeeper, if necessary

2. Edit Kafka config file

    vi ./config/server.properties
    set "zookeeper.connect":

        zookeeper.connect=localhost:2181/kafka

3. Start Kafka:

    nohup ./bin/kafka-server-start.sh ./config/server.properties > kafka.out &

4. Create Kafka topic:

   First check existing topics:

     ./bin/kafka-topics.sh --list --zookeeper localhost:2181/kafka

   Now create new topic for CnRssPoller

     ./bin/kafka-topics.sh --create --zookeeper localhost:2181/kafka \
       --replication-factor 1 --partitions 1 --topic cnrp-nrt-feed

   Now check that topic has been created check existing topics:

     ./bin/kafka-topics.sh --list --zookeeper localhost:2181/kafka

5. Start a Kafka Consumer

    /usr/local/kafka_2.11-0.11.0.0/bin/kafka-console-consumer.sh \
      --bootstrap-server localhost:9092                          \
      --topic cnrp-nrt-feed                                      \
      --from-beginning

      AND/OR

    {CN_RSS_POLLER_HOME}/utils/kafka/test_kafka_consumer.py

    NOTE: you can run multiple consumers for the same Kafka topic.

...  copy from other Readme's in this project...







