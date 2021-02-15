#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
########################################################################
# file:    test_kafka_producer_multi_msgs.py
# author:  rbw
# date:    Mon Feb 15 13:40:54 EST 2021
# purpose: implement a simple Kafka producer.
########################################################################
from kafka import KafkaProducer
from kafka.errors import KafkaError

kafka_servers = ['localhost:9092']
#kafka_topic = 'test-20181101'
kafka_topic = 'test'
kafka_msg = b'This is a test message - 1107'
kafka_msg_list = [ \
  'msg-1',         \
  'msg-2',         \
  'msg-3',         \
  'msg-4']

prod = KafkaProducer(bootstrap_servers=kafka_servers)

for msg in kafka_msg_list:
    print("sending message \"%s\"" % msg)
    future = prod.send(kafka_topic, msg)

try:
    rec_metadata = future.get(timeout=10)
except KafkaError:
    #log.exception()
    pass

print("topic:     " + str(rec_metadata.topic))
print("partition: " + str(rec_metadata.partition))
print("offset:    " + str(rec_metadata.offset))

