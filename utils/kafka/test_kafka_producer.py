#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
########################################################################
# file:    test_kafka_producer.py
# author:  rbw
# date:    Fri Aug  3 17:11:07 PDT 2018
# purpose: implement a simple Kafka producer.
########################################################################
from kafka import KafkaProducer
from kafka.errors import KafkaError

kafka_servers = ['localhost:9092']
#kafka_topic = 'test-20181101'
kafka_topic = 'test'
kafka_msg = b'This is a test message - 1107'

prod = KafkaProducer(bootstrap_servers=kafka_servers)

future = prod.send(kafka_topic, kafka_msg)

try:
    rec_metadata = future.get(timeout=10)
except KafkaError:
    #log.exception()
    pass

print "topic:     " + str(rec_metadata.topic)
print "partition: " + str(rec_metadata.partition)
print "offset:    " + str(rec_metadata.offset)

