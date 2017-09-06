#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    ut_cn_hpe_json_kafka_producer.py
# date:    Wed Aug 30 18:01:14 PDT 2017
# purpose: Unit Test for cn_hpe_json_kafka_producer.py
########################################################################
# import os, sys, time, re, anydbm
# import sys, os
from cn_hpe_json_kafka_producer import CnHpeJsonKafkaProducer

td1 = {}
td1['path'] =    "/data1/cn/rss_raw/2017/09/05/23/cn_rss_raw-news.australia.sydneymorningherald-20170905.2334.13.xml"
td1['src'] =     "news.australia.sydneymorningherald"
td1['tstamp'] =  "20170905.2334.13"
td1['pubdate'] = ""
td1['author'] =  ""
td1['guid'] =    "gyb4cv"
td1['url'] =     "http://smh.com.au/domain/domain-news/features/outer-pockets-offer-a-way-into-the-market-for-first-home-buyers-20170905-gyb4cv.html"
td1['title'] =   "Outer pockets offer a way into the market for first home buyers"
td1['summary'] = ""
td1['text1'] = \
"""
While they may be a little further out from the city than for generations
    past, there are still areas that may offer first home buyers an opportunity
to get their foot in the market.
"""

td2 = {}
td2['path'] =    "/data1/cn/rss_raw/2017/09/05/23/cn_rss_raw-aggr.memeo.all-20170905.2336.13.xml"
td2['src'] =     "aggr.memeo.all"
td2['tstamp'] =  "20170905.2336.13"
td2['pubdate'] = ""
td2['author'] = ""
td2['guid'] =    "http://www.memeorandum.com/170905/p114#a170905p114"
td2['url'] =     "http://www.memeorandum.com/170905/p114#a170905p114"
td2['title'] =   \
"""
Hurricane Irma isn't what Puerto Rico needs right now (Jill Disis/CNNMoney)"
"""
td2['summary'] = ""
td2['text1'] = \
"""
Jill Disis /  CNNMoney :
Hurricane Irma isn't what Puerto Rico needs
right now   &nbsp; &mdash;&nbsp; Puerto Rico's debt crisis explained&nbsp;
&mdash;&nbsp; Puerto Rico is in the path of a powerful new hurricane, and
it couldn't come at a worse time for the broke U.S. territory.&nbsp; &mdash;&nbsp;
Hurricane Irma &mdash; now a Category 5 storm with 185 mph winds &hellip;
"""

td3 = {}
td3['start-item'] = ""
td3['path'] =       "/data1/cn/rss_raw/2017/09/05/23/cn_rss_raw-news.newzealand.hawkesbay-20170905.2355.13.xml"
td3['src'] =        "news.newzealand.hawkesbay"
td3['tstamp'] =     "20170905.2355.13"
td3['pubdate'] =    ""
td3['author'] =     ""
td3['guid'] =       "gybn61"
td3['url'] =        "http://theage.com.au/business/media-and-marketing/facebooks-750m-push-for-cricket-rights-shows-theres-a-new-big-player-in-sports-20170905-gybn61.html"
td3['title'] =      \
"""
Facebook's $750m push for cricket rights shows there's a new big player in
sports
"""
td3['summary'] =    ""
td3['text1'] = \
"""
With a cash pile of $US6.25 billion, Facebook will have more shots at bidding
for live sporting events as it seeks to keep people glued to its expanding
media network, even as it missed out on the Indian Premier League.
"""

print "td1:"
print td1
print "td2:"
print td2
print "td3:"
print td3
print "td3['text1']"
print td3['text1']


cnj = CnHpeJsonKafkaProducer("")
cnj.say_hello()
