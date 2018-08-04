#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
########################################################################
# file:    test_kafka_consumer.py
# author:  rbw
# date:    Sat Aug  4 09:42:07 PDT 2018
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
kafka_topic = 'rbw-test-20180804-1105'

consumer = KafkaConsumer(kafka_topic)

for msg in consumer:
    print "msg.topic:     %s" % msg.topic
    print "msg.partition: %d" % msg.partition
    print "msg.offset:    %d" % msg.offset
    print "msg.key:       %s" % msg.key
    print "msg.value:     %s" % ""
    print "%s" % msg.value
    print ""

