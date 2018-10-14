#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
########################################################################
# file:    cnrp_passthru_processor.py
# author:  rbw
# date:    Wed Oct 10 17:09:39 PDT 2018
# purpose: implement a template processor that consumes data from a
#          Kafka topic and sends that data to another Kafka topic.
########################################################################
import os
import sys
import time
import json

from kafka import KafkaConsumer
from kafka.errors import KafkaError


