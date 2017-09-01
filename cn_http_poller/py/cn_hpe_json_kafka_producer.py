#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    cn_hpe_json_kafka_producer.py
# date:    Wed Aug 30 18:01:14 PDT 2017
# purpose: write RSS data, in JSON format to Kafka topic
########################################################################
# import os, sys, time, re, anydbm
import sys, os


class CnHpeJsonKafkaProducer():
    def __init__(self, kafka_broker_url):
        self.kafka_broker_url = kafka_broker_url

    def say_hello(self):
        print "Hello from CnHpeJsonKafkaProducer()"
