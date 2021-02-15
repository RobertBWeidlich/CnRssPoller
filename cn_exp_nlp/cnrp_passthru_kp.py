#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################################################################
# file:    cnrp_passthru_processor.py
# author:  rbw
# date:    Mon Feb 15 13:40:54 EST 2021
# purpose: implement a template processor that consumes data from a
#          Kafka topic and sends that data to another Kafka topic.
########################################################################
import os
import sys
import time
import json

from kafka import KafkaConsumer
from kafka.errors import KafkaError


