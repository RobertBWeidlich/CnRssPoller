#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################################################################
# file:    cn_hpe_json_kafka_producer.py
# date:    Mon Feb 15 13:40:54 EST 2021
# purpose: write RSS data, in JSON format to Kafka topic
########################################################################
# import os, sys, time, re, anydbm
import sys, os
from kafka import KafkaProducer


class CnHpeJsonKafkaProducer():

    def __init__(self, kafka_broker_url, kafka_topic):
        self.kafka_broker_url = kafka_broker_url
        self.kafka_topic = kafka_topic
        print("CnHpeJsonKafkaProducer() ctor")
        print("kafka_broker_url: %s" % kafka_broker_url)
        print("kafka_topic : %s" % kafka_topic)
        # assert isinstance(self.kafka_broker_url, object)
        self.kafka_producer = KafkaProducer(bootstrap_servers=self.kafka_broker_url)

    def say_hello(self):
        print("Hello from CnHpeJsonKafkaProducer()")

    def send_json_to_kafka(self, json_msg):
        self.kafka_producer.send(self.kafka_topic, json_msg)
        self.kafka_producer.flush()
        # convert to byte??
