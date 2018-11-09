#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
########################################################################
# file:    test_kafka_consumer.py
# author:  rbw
# date:    Thu Nov  1 16:15:57 PDT 2018
# purpose: implement a simple Kafka consumer.
########################################################################
import os
import sys
import time
import math
import json
import uuid

from kafka import KafkaConsumer
from kafka.errors import KafkaError

kafka_servers = ['localhost:9092']
##kafka_topic = 'cnrp-nrt-feed'
#kafka_topic = 'test-20181101'
kafka_topic = 'test'

consumer = KafkaConsumer(kafka_topic, bootstrap_servers=kafka_servers)
print "starting Kafka consumer"
print "Kafka servers: %s" % kafka_servers
print "Kafka topic:   %s" % kafka_topic

a = consumer.assignment()
print "assignment: %s" % str(a)

#b = consumer.beginning_offsets([0])
#print "beginning_offsets: %s" % str(b)

for msg in consumer:
    print "msg.topic:     %s" % msg.topic
    print "msg.partition: %d" % msg.partition
    print "msg.offset:    %d" % msg.offset
    print "msg.key:       %s" % msg.key
    print "msg.value:     \"%s\"" % msg.value
    #print "%s" % msg.value
    print ""

