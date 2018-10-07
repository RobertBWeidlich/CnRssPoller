file:    Readme-kafka.md
author:  rbw
date:    Mon Oct  1 13:41:59 PDT 2018
purpose: Addition of Kafka to CnRssPoller

Version 2.0 Polls a number of RSS Feeds, and sends the de-duped text to
a Kafka topic.

Follow these instructions to install and run.  This deployment consists
of multiple Linux windows:

1. Download and install Zookeeper, then start it, if necessary

    [Window-1] - monitor Kafka and Solr parameters maintained by Zookeeper
      ./zookeeper-client
        ls /solr
        ls /kafka
        ...

2. Download and install Kafka, if necessary

   Edit Kafka config file

    vi ./config/server.properties
    set "zookeeper.connect":

        zookeeper.connect=localhost:2181/kafka

3. Start Kafka:

    [Window-2]
    cd {KAFKA_INSTALL_DIR}
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

    [Window-3]
    /usr/local/kafka_2.11-0.11.0.0/bin/kafka-console-consumer.sh \
      --bootstrap-server localhost:9092                          \
      --topic cnrp-nrt-feed                                      \
      --from-beginning

      AND/OR

    {CN_RSS_POLLER_HOME}/utils/kafka/test_kafka_consumer.py

    NOTE: you can run multiple consumers for the same Kafka topic.

...  copy from other Readme's in this project...







