file:    Readme-2.0.md
author:  rbw
date:    Fri Oct 19 17:38:30 EDT 2018
purpose: Addition of Kafka to CnRssPoller

Version 2.0 polls a number of RSS Feeds, and sends the de-duped text to
a Kafka topic.

Follow these instructions to install and run.  This deployment consists
of multiple Linux windows, designated below as [Window-X]:

Also see the Readme-1.0.md file to set up the correct environmental
variables. [Todo: consolidate the Readme files to make this file
standalone]

1. Download and install Zookeeper, then start it if necessary.

   It's also possible to use Kafka's built-in Zookeeper server if
   zookeeper is not already installed.  These are the steps to run
   the built-in Zookeeper server:

    [Window-1]
      rm -rf /tmp/zookeeper
      cd /usr/local/kafka_2.11-2.0.0
      vi ./config/zookeeper.properties
      nohup ./bin/zookeeper-server-start.sh ./config/zookeeper.properties \
        > zk.out &

    [Window-2] - to monitor Kafka and Solr parameters maintained by Zookeeper
      zookeeper-client (for conventional zookeeper)
        ls /solr
        ls /kafka
        ...

2. Download and install Kafka, if necessary

   Edit Kafka config file

    [Window-3]
    vi ./config/server.properties
    set "zookeeper.connect":

        zookeeper.connect=localhost:2181/kafka

3. Start Kafka:

    [Window-3]
    cd {KAFKA_INSTALL_DIR}
    rm -rf /tmp/kafka-logs
    nohup ./bin/kafka-server-start.sh ./config/server.properties > kafka.out &

4. Create Kafka topic if necessary:

   First check existing topics:

    [Window-4]
     ./bin/kafka-topics.sh --list --zookeeper localhost:2181/kafka

   Now create new topic for CnRssPoller

     ./bin/kafka-topics.sh --create --zookeeper localhost:2181/kafka \
       --replication-factor 1 --partitions 1 --topic cnrp-nrt-feed

   Now check that topic has been created check existing topics:

     ./bin/kafka-topics.sh --list --zookeeper localhost:2181/kafka

5. Start a Kafka Consumer

    [Window-5]
    /usr/local/kafka_2.11-0.11.0.0/bin/kafka-console-consumer.sh \
      --bootstrap-server localhost:9092                          \
      --topic cnrp-nrt-feed                                      \
      --from-beginning

      AND/OR

    [Window-6]
    {CN_RSS_POLLER_HOME}/utils/kafka/test_kafka_consumer.py

    NOTE: you can run multiple consumers for the same Kafka topic.

...  copy from other Readme's in this project...

6. Start the two CN RSS processes.  

    [Window-7] 
      su - cn
      cd $CN_HOME
      ./cn_hpe.py ../config/cn_hpe.cfg

    [Window-8] 
      su - cn
      cd $CN_HOME
      ./cn_rss_proc_json_kafka.py

