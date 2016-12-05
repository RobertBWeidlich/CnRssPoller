#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# file:    ut_cn_hp_thr.py 
# author:  rbw
# date:    100920.1940
# purpose: Unit test for cn_hp_thr.py
########################################################################
import sys, urllib, time
import threading
import random
from cn_hp_thr import cn_hp_thr

logmutex = threading.Lock()
threads = []

url1 = 'http://rss.cnn.com/rss/cnn_topstories.rss'
url2 = 'http://rss.cnn.com/rss/cnn_latest.rss'
url3 = 'http://feeds.digg.com/digg/news/popular.rss'

out_id1 = 'news.cnn.topstories'
out_id2 = 'news.cnn.latest'
out_id3 = 'aggr.digg'

out_file1 = 'cn-news.cnn.topstories.xml'
out_file2 = 'cn-news.cnn.latest.xml'
out_file3 = 'cn-aggr.digg.xml'

thread = cn_hp_thr(out_id1, url1, out_file1, logmutex)
thread.start()
threads.append(thread)

thread = cn_hp_thr(out_id2, url2, out_file2, logmutex)
thread.start()
threads.append(thread)

thread = cn_hp_thr(out_id3, url3, out_file3, logmutex)
thread.start()
threads.append(thread)

for  thread in threads:
  thread.join()

print 'Main thread exiting'

sys.exit(0)


