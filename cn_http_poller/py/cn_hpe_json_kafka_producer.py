#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    cn_hpe_json_kafka_producer.py
# date:    Wed Aug 30 18:01:14 PDT 2017
# purpose: write RSS data, in JSON format to Kafka topic
########################################################################
# import os, sys, time, re, anydbm
import sys, os
from kafka import KafkaProducer


class CnHpeJsonKafkaProducer():
    def __init__(self, kafka_broker_url, kafka_topic):
        self.kafka_broker_url = kafka_broker_url
        self.kafka_topic = kafka_topic
        print "CnHpeJsonKafkaProducer() ctor"
        # assert isinstance(self.kafka_broker_url, object)
        self.kafka_producer = KafkaProducer(bootstrap_servers=self.kafka_broker_url)
        # self.kafka_producer = KafkaProducer()

    def say_hello(self):
        print "Hello from CnHpeJsonKafkaProducer()"

    def send_json_to_kafka(self, json_msg):
        self.kafka_producer.send(self.kafka_topic, json_msg)
        self.kafka_producer.flush()
        # convert to byte??

